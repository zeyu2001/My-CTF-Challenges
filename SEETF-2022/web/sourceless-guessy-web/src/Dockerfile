FROM php:8.1-apache

COPY index.php phpinfo.php main.css whysoserious /var/www/html/
COPY apache2.conf /etc/apache2/
RUN chmod +r /etc/apache2/apache2.conf

RUN chown -R root:root /var/www/
RUN chmod -R 755 /var/www/

RUN sed -i "s/Listen 80/Listen 8080/" /etc/apache2/ports.conf 

RUN echo "SEE{2nd_fl4g_n33ds_RCE_g00d_luck_h4x0r}" >> /etc/passwd
COPY readflag.c /readflag.c
RUN gcc -o /readflag /readflag.c && rm /readflag.c
RUN chmod +rxs /readflag

COPY flag.txt /root/flag.txt

USER www-data