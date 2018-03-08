def calculation(number_of_boxes, bbox):
    """
    Divide the BBOX of the City of Amsterdam in x number of quadrants/rectangles for use in limiting WFS/geo queries.

    Args:
        1. number_of_boxes: in multiples of 2, 8 works well for most cases.
        2. bbox: [110200,476772,134030,493900]
    Returns:
        list of quadrants [[x1,y1,x2,y2],[..]]
    """

    width = ((bbox[2] - bbox[0])/number_of_boxes)
    height = bbox[3] - bbox[1]
    bboxtotalset = []
    for i in range(0, number_of_boxes + 1):
        x = i
        y = number_of_boxes - 1 - i
        bboxtotalset.append([bbox[0] + width * x, bbox[1], bbox[2] - width * y, bbox[3]])
    bboxtotal = []
    quadrants_list = []

    for b in bboxtotalset:
        rightbottom = [b[0] + (width/2), b[1], b[2], b[3]-(height/2)]
        righttop = [b[0] + (width/2), b[1] + (height/2), b[2], b[3]]
        leftbottom = [b[0], b[1], b[2] - (width/2), b[3] - (height/2)]
        lefttop = [b[0], b[1] + (height/2), b[2] - (width/2), b[3]]

        quadrants = [lefttop, righttop, leftbottom, rightbottom]
        bboxtotal.append(quadrants)

    for q in bboxtotal:
        for i in q:
            # print "point(%s %s)" % (i[0],i[1])
            # print "point(%s %s)" % (i[2],i[3])
            bbox_quadrants = "%s,%s,%s,%s" % (i[0], i[1], i[2], i[3])
            quadrants_list.append(bbox_quadrants)

    return quadrants_list
