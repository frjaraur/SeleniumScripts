import sys, getopt, yaml,os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 

# browser = webdriver.Firefox()

# browser.get('http://www.google.com')
# assert 'Google' in browser.title

# elem = browser.find_element_by_name('q')  # Find the search box
# elem.send_keys('seleniumhq' + Keys.RETURN)
# time.sleep(10)
# browser.quit()


class Config:
    def __init__(self, configfile):
        with open(configfile) as f: configuration=yaml.safe_load(f)
        self.configuration=configuration
	
    def TestsConfig(self,root):
        return self.configuration[root]


def showhelp(vmyname):
   print ("HELP (" + vmyname + ")")
   sys.exit(2)

def exectest(vtesttasks):
    #Initialize Web Browser Driver
    browser = webdriver.Firefox()
    element=None
    taskresults=[False,None,False,None,element]

    print (str(len(taskresults)))
    for vtask in vtesttasks:
        print (str(len(taskresults)))
        # if len(taskresults) == 4:
        #     taskresults=executetask(browser,vtask,None)
        # else:
        taskresults=executetask(browser,vtask,taskresults[4])

    time.sleep(10)


    browser.quit()

def executetask(vbrowser, vtask,velement):
    print ("TASK --> "+vtask )
    tmp=vtask.split()
    command=tmp.pop(0)
    arguments=[]
    rtask=True
    rtext=None
    rfound=False
    rtimespend=None
    relement=velement
    results=[rtask,rtext,rfound,rtimespend,relement]
    for I in tmp:
        arguments.append(int(I)) if I.isdigit() else arguments.append(str(I))

    #print("command: "+command)
    #print ("arguments: "+ str(arguments))
    print ("ARG COUNT=> "+ str(len(arguments)))
    while command:
        if command == "open":
            vbrowser.get(arguments)
            break
        if command == "set_page_load_timeout" :
            vbrowser.set_page_load_timeout(arguments[0])
            break
        if command == "close" :
            time.sleep(5)
            vbrowser.close()
            break
        if command == "find_element_by_name":
            relement=vbrowser.find_element_by_name(arguments[0])
            print ("Devolvemos elemento....")
            break
        if command == "send_keys":
            velement.send_keys(arguments[0])
            break
        if command == "send_submit":
            velement.submit()
            break
        if command == "find_element_by_xpath_and_click":
            print (str(arguments[0]))
            vbrowser.find_element_by_xpath(arguments[0]).click()
            #vbrowser.find_element_by_xpath(str(arguments[0])).click()
            break
        if command == "find_element_by_partial_link_text":
            print (str(arguments[0]))
            vbrowser.find_element_by_partial_link_text(str(arguments[0])).click()
            #vbrowser.find_element_by_xpath(str(arguments[0])).click()
            break
        if command == "find_elements_by_xpath":
            #jokes = [str(joke.text) for joke in vbrowser.find_elements_by_xpath("//div/p[starts-with(@id,'joke_')]")]
            print (arguments[0])
            #links = [str(links) for links in vbrowser.find_elements_by_xpath(arguments[0])]
            links = vbrowser.find_elements_by_xpath(arguments[0])
            print (links)
            for a in links:
                print(a.get_attribute('href'))
            break
        if command == "mytest":
            links = vbrowser.find_elements_by_tag_name('li')
            print (links)
            for a in links:
                print()
                print (a)
                print(a.text)
                print()
            break

        print ("Command not found")
        rtask=False
        break
    results=[rtask,rtext,rfound,rtimespend,relement]
    return results

def main(argv):
    global debug, tasksfile
    tasksfile=""
    debug = False
    myname = os.path.basename(__file__)
    testsnames = list()
    testtasks = list()
    try:
      opts, args = getopt.getopt(argv, "Dht:", ["tasksfile=", "debug"])
    except getopt.GetoptError:
      showhelp(myname)

    for opt, arg in opts:
      if opt == '-h':
        showhelp(myname)
      elif opt in ("-D", "--debug"):
        debug = True
        print ("DEBUG MODE")
      elif opt in ("-t", "--tasksfile="):
        tasksfile=arg
      
    if tasksfile == '':
        print ("At least specify on tasksfile ... \n")
        showhelp(myname)
      
    tasksfile=Config(tasksfile)
    testsconfigs=tasksfile.TestsConfig("SELENIUM_TESTS")
    #print(testsconfigs)
    testsnames=testsconfigs.keys()
    for name in testsnames:
        print (name)
        print (testsconfigs[name])
        testtasks=testsconfigs[name]
        exectest(testtasks)
    
	
	
	
	
	
if __name__ == "__main__":
    main(sys.argv[1:])      
