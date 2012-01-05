'''
    Draft Creation Test
    ~~~~~~~~~~~~~~~~~~~

    Tests creating drafts.

    :copyright: Copyright 2011 by Vlad Riscutia
    :license: FreeBSD, see LICENSE file
'''
import datetime
import os
import tinkerer
from tinkerer import draft, master, page, post
import utils


# test creating drafts
class TestDraft(utils.BaseTinkererTest):
    # test creating draft from title
    def test_create(self):
        # create draft with given title
        new_draft = draft.create("My Draft")

        self.assertEquals(
                os.path.abspath(os.path.join(
                                    utils.TEST_ROOT, 
                                    "drafts", 
                                    "my_draft.rst")),
                new_draft)                                        

        self.assertTrue(os.path.exists(new_draft))


    # test moving draft from existing files
    def test_move(self):
        # create a post and a page
        new_post = post.create("A post", datetime.datetime(2010, 10, 1))
        new_page = page.create("A page")
        
        # page and posts should be in master doc (precondition)
        lines = master.read_master()
        self.assertIn("   %s\n" % new_post.docname, lines)
        self.assertIn("   %s\n" % new_page.docname, lines)

        new_draft = draft.move(os.path.join(
                            utils.TEST_ROOT, "pages", "a_page.rst"))
        self.assertTrue(os.path.exists(new_draft))

        # page should no longer be in TOC
        lines = master.read_master()
        self.assertIn("   %s\n" % new_post.docname, lines)
        self.assertNotIn("   %s\n" % new_page.docname, lines)

        new_draft = draft.move(os.path.join(
                            utils.TEST_ROOT, "2010", "10", "01", "a_post.rst"))
        self.assertTrue(os.path.exists(new_draft))

        # post should no longer be in TOC either
        lines = master.read_master()
        self.assertNotIn("   %s\n" % new_post.docname, lines)
        self.assertNotIn("   %s\n" % new_page.docname, lines)


    # test content
    def test_content(self):
        # create draft with no content
        new_draft = draft.create("My Draft")

        # check expected empty post content
        with open(new_draft) as f:
            self.assertEquals(f.readlines(),
                    ["My Draft\n",
                     "========\n",
                     "\n",
                     "\n",
                     "\n",
                     ".. author:: default\n",
                     ".. categories:: none\n",
                     ".. tags:: none\n",
                     ".. comments::\n"])
