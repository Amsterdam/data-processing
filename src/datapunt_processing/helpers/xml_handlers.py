######################################################################
# XML helper functions to manipulate XML feeds or objects
######################################################################

from lxml import etree 

def parse_and_remove(filename, path):
    """
    incremental XML parsing
    Args:
        filename: xml file name
        path: path to xml file
    source: 
        https://github.com/dabeaz/python-cookbook/blob/master/src/6/incremental_parsing_of_huge_xml_files/example.py
    """
    path_parts = path.split('/')
    doc = etree.iterparse(filename, ('start', 'end'))
    # Skip the root element
    next(doc)

    tag_stack = []
    elem_stack = []
    for event, elem in doc:
        if event == 'start':
            tag_stack.append(elem.tag)
            elem_stack.append(elem)
        elif event == 'end':
            if tag_stack == path_parts:
                yield elem
                elem_stack[-2].remove(elem)
            try:
                tag_stack.pop()
                elem_stack.pop()
            except IndexError:
                pass