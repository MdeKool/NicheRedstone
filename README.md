# Niche Redstone Backend Webserver
This repo contains the code for the webserver that can be used along with the
[Niche Redstone](https://www.curseforge.com/minecraft/mc-mods/niche-redstone) mod for Minecraft.
It works by running a FastAPI webserver using `docker compose` which serves files HTML files with the Jinja2 template style.

The project consists of the `webserver` container and an `Nginx` container.

## Setup
check whether the IP in the `proxy_pass` field in `nginx.conf` is correct by running `docker compose up -d`
and then `docker container inspect webserver | grep IPAddress`. If the IP address is different from the one specified
by `proxy_pass`, change the IP `proxy_pass` points to to the IPAddress you got.

It's not required, but I highly recommend creating an SSL certificate to enable HTTPS traffic to your server.
If you do not want to do this, you can skip to [Running](#Running).

If you want to enable HTTPS traffic, there's some steps you'll need to take.

---

Firstly, uncomment the lines in the `ports` and `volumes` definitions of the `nginx` container in `docker-compose.yml`.
Then, uncomment the lines in the `HTTPS` block and comment the ones in the `HTTP` block of `nginx.conf`. 

After that, you'll need to make an SSL certificate.

### Let's Encrypt
If you own a registered domain name you can easily do this with [Let's Encrypt](https://letsencrypt.org/getting-started/). 
This will give you some `*.pem` files in `/etc/letsencrypt/live/YOUR_DOMAIN/`.

Once you have these, go to `nginx.conf`:
- Change the path for `ssl_certificate` to point to your `cert.pem`.
- Change the path for `ssl_certificate_key` to point to your `privkey.pem`.

### OpenSSL

If you do not own a registered domain
name, but you do own/rent a server, you can create an SSL certificate with OpenSSL by following 
[these steps](https://gist.github.com/KeithYeh/bb07cadd23645a6a62509b1ec8986bbc).

Once you have a valid certificate, change the paths in `nginx.conf`:
- `ssl_certificate` should point to your `*.crt` file
- `ssl_certificate_key` should point to your `*.key` file

---

### Verifying
You can verify that everything is running as it is supposed to by trying to run `docker compose up` and 
checking the output of the nginx container.

## Running

Once you have completed the setup run `docker compose up -d`.
The webserver binds to port 8000 by default.

---

This is still a WIP, the `plans` page will eventually show the plans for future improvements to
the mod and this project
