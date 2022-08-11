import argparse
import datasets
import xmlrpc.client

# The core part is mostly a copy/paste from zmifanva/web.


def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', required=True)
    parser.add_argument('--endpoint', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--src-field', required=True)
    parser.add_argument('--tgt-field', required=True)
    return parser.parse_args()


PUNC_ENTITY_MAP = [
    # ('&', '&amp;'),  # handle specially
    ('|', '&#124;'),
    ('<', '&lt;'),
    ('>', '&gt;'),
    ('\'', '&apos;'),
    ('"', '&quot;'),
    ('[', '&#91;'),
    (']', '&#93;')
]


def escape_html_entities(text):
    text = text.replace('&', '&amp;')
    for punc, entity in PUNC_ENTITY_MAP:
        text = text.replace(punc, entity)
    return text


def unescape_html_entities(text):
    for punc, entity in PUNC_ENTITY_MAP:
        text = text.replace(entity, punc)
    text = text.replace('&amp;', '&')
    return text


def translate_sentence(moses_server, sentence):
    src = escape_html_entities(sentence)
    tr = moses_server.translate({'text': src})
    tgt = tr['text']
    tgt = unescape_html_entities(tgt)
    tgt = tgt.lower()
    return tgt


def translate(ds, moses_server, src_field, tgt_field):
    new_splits = {}
    for name, split in ds.items():
        sentences = split[src_field]
        translations = [
                translate_sentence(moses_server, sentence)
                for sentence in sentences]
        new_splits[name] = split.add_column(tgt_field, translations)
    for name, split in new_splits.items():
        ds[name] = split


def main():
    args = parse_command_line()
    moses_server = xmlrpc.client.ServerProxy(args.endpoint)
    ds = datasets.load_from_disk(args.dataset)
    translate(ds, moses_server, args.src_field, args.tgt_field)
    ds.save_to_disk(args.output)


main()
