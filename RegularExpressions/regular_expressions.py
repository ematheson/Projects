# regular_expressions.py
"""Volume 3: Regular Expressions.
<EM>
<Vol3A, 403>
<14 Sept, 2017>
"""
'''
all the same!!
a,b = 1,0
a,b = [1,0]
a,b = (1,0)

'''
import re

# Problem 1
def prob1():
    """Compile and return a regular expression pattern object with the
    pattern string "python".

    Returns:
        (_sre.SRE_Pattern): a compiled regular expression pattern object.
    """
    return re.compile("python")

# Problem 2
def prob2():
    """Compile and return a regular expression pattern object that matches
    the string "^{@}(?)[%]{.}(*)[_]{&}$".

    Returns:
        (_sre.SRE_Pattern): a compiled regular expression pattern object.
    """
    return re.compile(r"\^\{@\}\(\?\)\[%\]\{\.\}\(\*\)\[_\]\{&\}\$")

# Problem 3
def prob3():
    """Compile and return a regular expression pattern object that matches
    the following strings (and no other strings).

        Book store          Mattress store          Grocery store
        Book supplier       Mattress supplier       Grocery supplier

    Returns:
        (_sre.SRE_Pattern): a compiled regular expression pattern object.
    """
    rb = r"^(Book|Mattress|Grocery) (store|supplier)$"
    return re.compile(rb)


# Problem 4
def prob4():
    """Compile and return a regular expression pattern object that matches
    any valid Python identifier.

    Returns:
        (_sre.SRE_Pattern): a compiled regular expression pattern object.
    """
    #starts with underscore or alphabetical letter
    p1 = r"^[_a-zA-Z]\w*$"
    # [ ] already ORs everything
    return re.compile(p1)


# Problem 5
def prob5(code):
    """Use regular expressions to place colons in the appropriate spots of the
    input string, representing Python code. 

    You may assume that every possible colon is missing in the input string.

    Parameters:
        code (str): a string of Python code without any colons.

    Returns:
        (str): code, but with the colons inserted in the right places.
    """
    #if you see a 'while', add : at end of line
    
    expr = re.compile(r"((?:if|elif|else|for|while|try|except|finally|with|def|class).*)\n")
    # ?: makes inner group () non-capturing 
     
            # other option is, instead of \n , to put $ at the end and add , re.MULTILINE

    return expr.sub( r"\1:\n" ,code)


# Problem 6
def prob6(filename="fake_contacts.txt"):
    """Use regular expressions to parse the data in the given file and format
    it uniformly, writing birthdays as mm/dd/yyyy and phone numbers as
    (xxx)xxx-xxxx. Construct a dictionary where the key is the name of an
    individual and the value is another dictionary containing their
    information. Each of these inner dictionaries should have the keys
    "birthday", "email", and "phone". In the case of missing data, map the key
    to None.

    Returns:
        (dict): a dictionary mapping names to a dictionary of personal info.
    """
    #[0-9] is [\d]

    bday_pat = re.compile(r"[0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4}")
    #mm/dd/yyyy (how we want it in the end)  Or  mm/d/yy
    email_pat = re.compile(r"[\w\.]+@[\.\w]+")

    phone_pat = re.compile(r"(?:1-)?\(?([0-9]{3})\)?-?([0-9]{3})-([0-9]{4})")

    # xxx or (xxx), so may or may not see ( or ) as well as a 1- in front
    #(xxx)xxx-xxxx (how we want it in the end), or xxx-xxx-xxxx, or 1-xxx-xxx-xxxx

    contacts_dict = {}

    with open(filename,'r') as File:

        line_list = File.readlines()

        for line in line_list:
            person = {}
                                
            name_pat = re.compile(r"^[A-Za-z]+ (?:[A-Z]\. )?[A-Za-z]+")
            #may or may not see a middle initial
            #use a line anchor ^, but no dollar sign

            name = name_pat.findall(line)
            phone = phone_pat.findall(line)
            email = email_pat.findall(line)
            bday = bday_pat.findall(line)# returns list w/ single string being the whole date

            if phone:
                phone = phone[0]
                person["phone"] = "({}){}-{}".format(phone[0], phone[1], phone[2])
            else:
                person["phone"] = None


            #print(email[0])
            if email:
                person["email"] = email[0]
                #if email wasn't found, it's already None
            else:
                person["email"] = None

            if bday:
                #print(bday)
                d,m,y = bday[0].split("/")

                #print(y)
                if len(d) ==1:
                    d = "0"+ d
                if len(m) ==1:
                    m = "0"+ m
                if len(y) ==2:
                    y = "20"+ y
                #print(y)

                person["birthday"] = "{}/{}/{}".format(d,m,y)

            else:
                person["birthday"] = None

            contacts_dict[name[0]] = person
            #inside the for loop!

    return contacts_dict


def testing(pattern, positive, negative):
    for x in positive:
        if not pattern.search(x):
            print("pattern was not found in "+x+" when it should have been")
    for y in negative:
        if pattern.search(y):
            print("pattern was found for "+y+ " when it wasn't supposed to be")


if __name__ == '__main__':
    #problem 1 testing
    pattern = prob1()
    pos_list = ['python', 'yo python', ' i love python whoo! ']
    neg_list = [ 'pi day', 'sspyuuthon' ]
    testing(pattern, pos_list, neg_list)
    #problem 2 testing
    pos = ["^{@}(?)[%]{.}(*)[_]{&}$", "379^{@}(?)[%]{.}(*)[_]{&}$2223"]
    neg = ["719"]
    pat2 = prob2()
    testing(pat2, pos, neg)
    #problem 3 testing
    p = ["Book store", "Mattress supplier", "Grocery store"]
    n = ["Book place", "Mattress firm", "Grocery Mattress supplier"]
    pat3 = prob3()
    testing(pat3, p, n)
    #problem 4 testing
    matches = ['Mouse', 'compile', '_123456789', '__x__', 'while']
    non_matches = ['3rats', 'err*r', 'sq(x)', 'sleep()', ' x']
    pat4 = prob4()
    testing(pat4, matches, non_matches)
    #problem 5 testing
    code = """
    k, i, p = 999, 1, 0
    while k > i
        i *= 2
        p += 1
        if k != 999
            print("k should not have changed")
        else
            pass
    print(p)
    """
    #print(prob5(code))
    #print(prob6("fake_contacts.txt"))