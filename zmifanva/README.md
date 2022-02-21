# zmifanva <-> Lojban  English Machine Translation Engine

Developed by Masato Hagiwara: <https://github.com/mhagiwara/zmifanva>, forked at <https://github.com/olpa/zmifanva/>.

## Build

As a prerequisite, build `moses-tune` image: <../moses/README.md>.

Build the images `zf-base`, `moses-zf-jb2en`, `moses-zf-en2jb`, `zmifanva`:

```
make all
```

## Run the web application

```
make run-zmifanva  # docker-compose up
xdg-open http://localhost:6543
```

Zmivanfa works on the port 6543. Open the start page in your browser: <http://localhost:6543>.

## Run the web application without docker-comose

Run three commands in three different consoles:

```
make run-jb2en
make run-en2jb
make run-zf-web
```

I wish you are lucky and `host_ip` is calculated correctly. Otherwise, set the variable in `Makefile` to a right value.

## Run the translator in the command line

On the host:

```
make run-zf-dev
```

In the container:

```
# For Lojban to English
moses -f /build/zmifanva/train.jb-en/model/moses.ini
# For English to Lojban
moses -f /build/zmifanva/train.en-jb/model/moses.ini
```

Write a sentence, press ENTER. Find a translation among output.

## Use the translator over XML-RPC

On example of Lojban to English. Start the container as an xmlrpc server:

```
make run-jb2en
```

Create `x.xml` with a payload for an xmlrpc request:

```
<?xml version="1.0"?>
<methodCall>
  <methodName>translate</methodName>
  <params>
    <param>
      <value>
        <struct>
          <member>
            <name>text</name>
            <value>
              <string>coi ro do</string>
            </value>
          </member>
          <member>
            <name>align</name>
            <value>
              <string>false</string>
            </value>
          </member>
          <member>
            <name>report-all-factors</name>
            <value>
              <string>false</string>
            </value>
          </member>
        </struct>
      </value>
    </param>
  </params>
</methodCall>
```

Make a call:

```
curl -d @x.xml http://localhost:8078/RPC2
```

Get the result:

```
<?xml version="1.0" encoding="UTF-8"?>
<methodResponse>
<params>
<param><value><struct>
<member><name>text</name>
<value><string>Hi , everybody . </string></value></member>
</struct></value></param>
</params>
</methodResponse>
```

For English to Lojban, use the makefile target `run-en2jb` and the port `8079`.


# Develop for zmifanva

- Fork the fork: <https://github.com/olpa/zmifanva/>
- Checkout your forked repository
- In `Makefile`, for the goal `run-dev`, update the binding of `/build/zmifanva` to your repository
- Start the development container:

```
$ make run-dev
```

Inside the container, start the server:

```
PYTHONPATH=/build/zmifanva/web pserve --reload /build/zmifanva/web/development.ini
```

The `pserve` tool automatically restarts the server after a change in Python files.
