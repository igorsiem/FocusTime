import sys
sys.path.insert(0, '../focustime')

from focustime.models.session import Session

def test_instantiation():
    """Test basic instantiation of the Session class

    1. A `Session` can be instantiated

    2. When a `Session` is instantiated, it has a `segments` member, which is
       an Array with zero elements.
    """

    s = Session()
    assert s != None
    assert hasattr(s, 'segments')
    assert len(s.segments) == 0
