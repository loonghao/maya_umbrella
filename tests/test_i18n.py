from maya_umbrella import i18n


def test_translator():
    translator = i18n.Translator()

    name = "maya.test.ma"
    assert translator.translate("start_fix_issues",
                                name=name) == "Start fixing all problems related to Maya virus maya.test.ma"

    translator.set_locale("zh_CN")
    assert translator.translate("start_fix_issues", name=name) == "开始修复与 Maya 病毒相关的所有问题 maya.test.ma"
