"""
Script to convert to a Apache Solr readable XML format
to bitext (tab-separated plain text) of Lojban and English.

Copy/paste from zmifanva project.
"""
import sys
import xml.etree.ElementTree as ET


def iterate_bitext(add_root_node):
    """Given the root node of XML ElementTree, yield bitext.

    Args:
        add_root_node: XML Element pointing to the root 'add' node of Solr doc.
    Returns:
        generator over tuples (jbo_t, eng_t) where
            jbo_t (string): Lojban text
            eng_t (string): English text)

    Skip the document if either field is missing or empty.
    """
    for doc_node in add_root_node:
        jbo_t = None
        eng_t = None
        id_ = None
        for field_node in doc_node:
            if field_node.attrib['name'] == 'id':
                id_ = field_node.text
            if field_node.attrib['name'] == 'jbo_t':
                jbo_t = field_node.text
            if field_node.attrib['name'] == 'eng_t':
                eng_t = field_node.text
        if not (id_ and jbo_t and eng_t):
            continue
        yield (id_, jbo_t, eng_t)


def main():
    """Main function"""
    if len(sys.argv) == 1:
        print("Usage: python convert_solr_xml_to_bitext.py "
              "[XML filename] > output text filename")
        sys.exit(1)

    for filename in sys.argv[1:]:
        tree = ET.parse(filename)
        root = tree.getroot()

        for id_, jbo_t, eng_t in iterate_bitext(root):
            print('%s\t%s\t%s' % (id_, jbo_t, eng_t))


if __name__ == '__main__':
    import codecs
    sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
    main()
