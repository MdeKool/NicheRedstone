# Niche Redstone Backend Webserver
This repo contains the code for the webserver that can be used along with the
[Niche Redstone](https://www.curseforge.com/minecraft/mc-mods/niche-redstone) mod for Minecraft.
It works by running a FastAPI webserver using `docker compose` which serves files HTML files with the Jinja2 template style.

The project consists of the `webserver` container and an `Nginx` container.

It should work on Linux installations out of the box, simply clone and run `docker compose up -d`.
The webserver binds to port 8000 by default.

This is still a WIP, the `plans` page will eventually show the plans for future improvements to
the mod and this project
