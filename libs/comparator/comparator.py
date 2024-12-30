from libs.comparator.ui.main_window import ListComparator

def comparate(parent_window):
    window = ListComparator()
    window.setParent(parent_window)
    window.show()
