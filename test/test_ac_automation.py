import pytest
from cmip.text.ac_automation import ACAutomation


def test_extract_keywords():
    aca = ACAutomation()
    aca.add_keywords_from_list(["bcdef", "fg", "cde"])
    expect = ["bcdef"]
    founds = aca.extract_keywords("abcdefg", all_mode=False)
    assert expect == founds
    expect = ['bcdef', 'cde', 'fg']
    founds = aca.extract_keywords("abcdefg", all_mode=True)
    assert expect == founds
    aca = ACAutomation()
    aca.add_keywords_from_list(["she", "shr", "say", "her", ])
    aca.add_keywords_from_list(["ashe", "sh"])
    expect = ['ashe', 'her']
    founds = aca.extract_keywords("yasherhs", all_mode=False, index_info=False)
    assert expect == founds
    expect = ['ashe', 'sh', 'she', 'her']
    founds = aca.extract_keywords("yasherhs", all_mode=True, index_info=False)
    assert expect == founds
    founds = aca.extract_keywords("yasherhs", all_mode=True, index_info=True)
    assert [x[0] for x in founds] == expect
    for x in founds:
        assert x[0] == "yasherhs"[x[1][0]:x[1][1]]


def test_replace_keywords():
    aca = ACAutomation()
    aca.add_keywords_from_list([("中国", "美国"), ("javascript", "pythonscript"), ("java", "c++"), "asc", "都会java"])
    sentence = "中国程序员都会java和javascript"
    expect = "美国序员都会c++和pythonscript"
    new = aca.replace_keywords(sentence)
    assert expect == new
