# -*- coding: UTF-8 -*-
import pytest

from maya_umbrella import i18n


def test_translator(monkeypatch):
    monkeypatch.setenv("MAYA_UMBRELLA_LANG", "en_US")
    translator = i18n.Translator()

    name = "maya.test.ma"
    assert translator.translate("start_fix_issues",
                                name=name) == "Start fixing all problems related to Maya virus maya.test.ma"

    translator.set_locale("zh_CN")
    assert translator.translate("start_fix_issues", name=name) == u"开始修复与 Maya 病毒相关的所有问题 maya.test.ma"


def test_set_locale(monkeypatch):
    translator = i18n.Translator()
    with pytest.raises(ValueError):
        translator.set_locale("zh_CN_xxx")
