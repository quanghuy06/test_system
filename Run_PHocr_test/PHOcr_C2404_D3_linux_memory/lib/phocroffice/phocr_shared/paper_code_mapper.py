# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.


class PaperCodeMapper(object):
    """
    This class is used to map a paper name to the corresponding paper code
    """

    DEFAULT = 0        # Default value
    LETTER = 1         # Letter size
    LEDGER = 3         # Ledger size
    LEGAL = 5          # Legal size
    STATEMENT = 6      # Statement size
    A3 = 8             # A3 size
    A4 = 9             # A4 size
    A5 = 11            # A5 paper size
    B4 = 12            # B4 paper size
    B5 = 13            # B5 paper size
    LG_13 = 41         # 13" LG paper size
    J_POST_CARD = 43   # Japanese Postcard paper size
    FOLIO = 60         # Folio paper size
    A6 = 70            # A6 paper size
    COMPUTER = 122     # Computer paper size
    SQ_85 = 123        # 8.5 SQ paper size
    K16 = 125          # 16K paper size
    K8 = 126           # 8K paper size

    # Paper code map
    paper_code_mapper_ = {
        "1stPage": DEFAULT,
        "original": DEFAULT,
        "Letter": LETTER,
        "Ledger": LEDGER,
        "Legal": LEGAL,
        "Statement": STATEMENT,
        "Computer": COMPUTER,
        "A3": A3,
        "A4": A4,
        "A5": A5,
        "B4": B4,
        "B5": B5,
        "13LG": LG_13,
        "JPostCard": J_POST_CARD,
        "Folio": FOLIO,
        "A6": A6,
        "8.5SQ": SQ_85,
        "16K": K16,
        "8K": K8,
    }

    @classmethod
    def get_paper_code(cls, paper_name):
        """
        Class method used to to get the paper code from paper name
        :return:
        """
        if paper_name in cls.paper_code_mapper_:
            return cls.paper_code_mapper_[paper_name]
        else:
            raise Exception(
                "Can't map {} to an valid PaperCode".format(paper_name))
