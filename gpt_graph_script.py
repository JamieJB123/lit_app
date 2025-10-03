# def add_book_to_graph(book: Dict):
    # create and merge book node (use a real unique key if possible)
    # book_node = Node("Book", title=book["title"], author=book.get("author"), year=book.get("year"))
    # graph.merge(book_node, "Book", "title")

    # multi-valued attributes
    # for attribute_key in BOOK_ATTRIBUTE_TYPES:
    #     values = book.get(attribute_key, []) or []
    #     label = ATTRIBUTE_LABEL_MAP.get(attribute_key, attribute_key.capitalize())

    #     for val in values:
            # support two formats: either string OR [name, weight]
            # if isinstance(val, (list, tuple)) and len(val) >= 1:
            #     name = val[0]
            #     weight = float(val[1]) if len(val) > 1 else None
            # else:
            #     name = val
            #     weight = None

            # if not name:
            #     continue

            # attr_node = Node(label, name=name)
            # graph.merge(attr_node, label, "name")         # ensures unique attribute node

            # rel = Relationship(book_node, f"HAS_{label.upper()}", attr_node)
            # if weight is not None:
            #     rel["weight"] = weight
            # graph.merge(rel)   # creates relationship if missing, updates properties if present

    # single-valued attributes: similar but a single node and relationship
    # for key in BOOK_ATTRIBUTE_TYPES_SINGLE_VAL:
    #     val = book.get(key)
    #     if val:
    #         label = key.title().replace("_", "")
    #         attr_node = Node(label, name=val)
    #         graph.merge(attr_node, label, "name")
    #         rel = Relationship(book_node, f"HAS_{label.upper()}", attr_node)
    #         graph.merge(rel)
