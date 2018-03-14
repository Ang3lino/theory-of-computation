#include <iostream>
#include <regex>
#include <string>

using namespace std;

int main(void) {
	string path = "(^(.+)/)?([^/]+)$",
		   valid_char = "([A-Z]|[a-z]|[0-9])",
		   include = "#include(([:stace:])?)((<((" + valid_char + ")+).h>))";
	string str;
	regex pattern(include);
	cin >> str;
	cout << regex_match(str, pattern) << endl;
	return 0;
}
