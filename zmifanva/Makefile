all: zmifanva jb2en en2jb

zf-base: .zf-base

.zf-base: Dockerfile.zf-base
	docker build -f $< -t zf-base .
	touch $@

jb2en: .zf-jb2en

.zf-jb2en: Dockerfile.moses-zf-jb2en zf-base
	docker build -f $< -t moses-zf-jb2en .
	touch $@

en2jb: .zf-en2jb

.zf-en2jb: Dockerfile.moses-zf-en2jb zf-base
	docker build -f $< -t moses-zf-en2jb .
	touch $@

zmifanva: .zmifanva

.zmifanva: Dockerfile.zmifanva zf-base
	docker build -f $< -t zmifanva .
	touch $@

# --

host_ip=$(shell ip -o addr show up primary scope global | grep '/24' | head -1 | sed 's@^.*inet @@' | cut -f 1 -d /)

networking=-p 6543:6543 \
  -e MOSES_SERVER_JB2EN=http://$(host_ip):8078 \
  -e MOSES_SERVER_EN2JB=http://$(host_ip):8079

run-dev:
	docker run -it \
	  -v $(shell pwd)/share:/share \
	  -v /home/olpa/p/zmifanva:/build/zmifanva \
	  $(networking) \
	  zf-base

run-zf-web:
	docker run $(networking) zmifanva

run-jb2en:
	docker run -it -p 8078:8080 moses-zf-jb2en

run-en2jb:
	docker run -it -p 8079:8080 moses-zf-en2jb

run-zmifanva:
	docker-compose up
