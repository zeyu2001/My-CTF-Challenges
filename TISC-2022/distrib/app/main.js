const crypto = require('crypto')
const util = require('util')

const pug = require('pug')
const mysql = require('mysql')

const express = require('express')
const session = require('express-session')
const RedisStore = require("connect-redis")(session)

const { createClient } = require("redis")
const redisClient = createClient({ 
    legacyMode: true, 
    url: 'redis://redis:6379'
})
redisClient.connect().catch(console.error)

const { doReportHandler } = require('./report.js')

const db = mysql.createConnection({
    host     : 'db',
    user     : 'web',
    password : process.env.MYSQL_PASSWORD,
    database : 'palindrome'
});
const query = util.promisify(db.query).bind(db);

const app = express()
const port = 8000

app.set('case sensitive routing', true)

app.use('/static', express.static('static'))
app.use(express.json())

app.use(session({
    secret: crypto.randomBytes(32).toString('hex'),
    resave: false,
    saveUninitialized: true,
    cookie: { maxAge: 1000 * 60 * 60 * 24 },
    store: new RedisStore({ client: redisClient })
}))

app.use((req, res, next) => {
    res.setHeader(
        'Content-Security-Policy',
        "default-src 'self'; img-src data: *; object-src 'none'; base-uri 'none'; frame-ancestors 'none'"
    )
    res.setHeader(
        'Cross-Origin-Opener-Policy',
        'same-origin'
    )
    next()
})

const authenticationMiddleware = async (req, res, next) => {
    if (req.session.userId) {
        if (req.ip === '127.0.0.1')
            req.session.token = process.env.ADMIN_TOKEN 

        next()
    }
    else 
        return res.redirect('/login')
}

const getLoginHandler = async (req, res) => {
    return res.send(pug.renderFile('templates/login.pug'))
}

const postLoginHandler = async (req, res) => {
    const { email, password } = req.body
    if (!email || !password)
        return res.status(400).send({ message: 'Missing email or password' })

    const rows = await query(`SELECT * FROM users WHERE email = ? AND password = ?`, [email, password])
    if (rows.length === 0)
        return res.status(401).send({ message: 'Invalid email or password' })

    req.session.userId = rows[0].id
    return res.status(200).send({ message: "Success" })
}

const indexHandler = async (req, res) => {
    return res.send(pug.renderFile('templates/index.pug'))
}

const reportIssueHandler = async (req, res) => {
    return res.send(pug.renderFile('templates/report.pug'))
}

const forbiddenHandler = async (req, res) => {
    return res.status(403).send(pug.renderFile('templates/forbidden.pug'))
}

const getTokenHandler = async (req, res) => {
    return res.send(pug.renderFile('templates/token.pug', { 
        token: req.session.token,
        username: req.session.username,
    }))
}

const postTokenHandler = async (req, res) => {

    const username = req.body.username

    if (!username)
        return res.status(400).send({ message: 'Missing username' })

    if (typeof username !== 'string')
        return res.status(400).send({ message: 'Invalid username' })

    let message

    if (!req.session.token) {

        const alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
        let tokenChars = []

        for (let i = 0; i < 10; i++ )
            tokenChars.push(alphabet.charAt(Math.floor(Math.random() * alphabet.length)))
        
        const token = 'TISC{' + tokenChars.join(':') + '}'

        try {
            const result = await query('INSERT INTO tokens (token, username) VALUES (?, ?)', [token, username])
        }
        catch (e) {
           return res.status(400).send({ message: e.message })
        }
        
        req.session.token = token
        req.session.username = username

        message = 'Token generated.'
    }
    else {
        message = `Sorry ${username}, you already have a token.`
    }

    return res.send({ token: req.session.token, username: req.session.username, message: message })
}

const tokenVerifyHandler = async (req, res) => {
    const token = req.query.token
    if (!token)
        return res.send(pug.renderFile('templates/verify.pug'))

    if (typeof token !== 'string')
    return res.status(400).send(pug.renderFile('templates/verify.pug', { error: 'Invalid token' }))
    
    const result = await query('SELECT * FROM tokens WHERE token = ?', [token])

    if (result.length == 0)
        return res.status(404).send(pug.renderFile('templates/verify.pug', { error: 'Token not found' }))

    const username = result[0].username
    return res.send(pug.renderFile('templates/verify.pug', { username: username, token: req.session.token }))
}

app.get     ('/login', getLoginHandler)
app.post    ('/login', postLoginHandler)

app.get     ('/index', authenticationMiddleware, indexHandler)
app.get     ('/token', authenticationMiddleware, getTokenHandler)
app.post    ('/token', authenticationMiddleware, postTokenHandler)
app.get     ('/verify', authenticationMiddleware, tokenVerifyHandler)
app.get     ('/report-issue', authenticationMiddleware, reportIssueHandler)
app.post    ('/do-report', authenticationMiddleware, doReportHandler)
app.all     ('/forbidden', authenticationMiddleware, forbiddenHandler)

app.listen(port, '0.0.0.0', async () => {
    console.log(`[*] Listening on port ${port}`)
})
