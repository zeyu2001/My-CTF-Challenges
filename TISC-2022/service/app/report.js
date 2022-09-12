const puppeteer = require('puppeteer')

const LOGIN_URL = `${process.env.BASE_URL}/login`
const TOKEN_URL = `${process.env.BASE_URL}/token`

let browser = null

const visit = async (url) => {
    const ctx = await browser.createIncognitoBrowserContext()
    const page = await ctx.newPage()

    await page.goto(LOGIN_URL, { timeout: 5000, waitUntil: 'networkidle2' })
    await page.waitForSelector('form')
    await page.type('input[name=email]', process.env.EMAIL)
    await page.type('input[name=password]', process.env.PASSWORD)
    await page.click('button[type="submit"]')
    await page.waitForTimeout(1000)

    try {
        await page.goto(url, { timeout: 5000, waitUntil: 'networkidle2' })
        await page.waitForTimeout(1000)
    } finally {
        await page.close()
        await ctx.close()
    }
}

const doReportHandler = async (req, res) => {

    if (!browser) {
        console.log('[INFO] Starting browser')
        browser = await puppeteer.launch({
            headless: false,
            args: [
                "--no-sandbox",
                "--disable-background-networking",
                "--disk-cache-dir=/dev/null",
                "--disable-default-apps",
                "--disable-extensions",
                "--disable-desktop-notifications",
                "--disable-gpu",
                "--disable-sync",
                "--disable-translate",
                "--disable-dev-shm-usage",
                "--hide-scrollbars",
                "--metrics-recording-only",
                "--mute-audio",
                "--no-first-run",
                "--safebrowsing-disable-auto-update",
                "--window-size=1440,900",
            ]
        })
    }

    const url = req.body.url
    if (
        url === undefined ||
        (!url.startsWith('http://') && !url.startsWith('https://'))
    ) {
        return res.status(400).send({ error: 'Invalid URL' })
    }

    try {
        console.log(`[*] Visiting ${url}`)
        await visit(url)
        console.log(`[*] Done visiting ${url}`)
        return res.sendStatus(200)
    } catch (e) {
        console.error(`[-] Error visiting ${url}: ${e.message}`)
        return res.status(400).send({ error: e.message })
    }
}

module.exports = { doReportHandler }