from lxml import etree


def xml_diff(change_xml, main_xml):
    parser = etree.XMLParser(remove_blank_text=True)  # initial pareser

    ''' xml to change '''
    _change_xml = etree.parse(change_xml, parser).getroot()
    tree_change = etree.XML(etree.tostring(_change_xml))

    ''' xml main '''
    _main_xml = etree.parse(main_xml, parser).getroot()
    tree_main = etree.ElementTree(_main_xml)

    ''' loop in main xml '''
    for e in _main_xml.iter():
        elem_find_path = str(tree_main.getelementpath(e))  # path element from main xml
        elem_parent = e.getparent()  # parent element if None 'e' is CONFIG
        find_elem = tree_change.find(elem_find_path)  # search element in xml to change if None then add this element

        if elem_parent is not None and find_elem is None:
            elem_insert = e.tag  # name of element
            elem_parent_path = str(tree_main.getelementpath(elem_parent))  # parent path
            elem_parent_change = tree_change.find(elem_parent_path)  # parent path element in xml to change
            child = etree.SubElement(elem_parent_change, elem_insert)  # add element to parent
            for a in e.attrib:  # add attributes to child
                child.set(a, e.attrib[a])

    return tree_change
