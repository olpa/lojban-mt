import argparse


def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--endpoint', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--src-field', required=True)
    parser.add_argument('--tgt-field', required=True)
    return parser.parse_args()


def translate(moses_server, sentence):


        # English to Lojban translation
        src = ' '.join(tokenize_en(src))
        src = escape_html_entities(src)
        try:
            tr = moses_server.translate({'text': src})
            tgt = tr['text']
        except Exception as e:
            return { 'tgt': '', 'error': 'Error calling moses: ' + str(e) }
        tgt = unescape_html_entities(tgt)
        return { 'tgt': tgt }
    else:

def main():
    args = parse_command_line()
    print(args)


main()
