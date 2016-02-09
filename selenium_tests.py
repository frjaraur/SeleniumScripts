import sys, getopt, yaml,os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 

class Config:
    def __init__(self, configfile):
        with open(configfile) as f: configuration=yaml.safe_load(f)
        self.configuration=configuration
    
    def TestsConfig(self,root):
        return self.configuration[root]


def showhelp(vmyname):
   print ("HELP (" + vmyname + ")")
   sys.exit(2)

def exectest(name,vtesttasks):
    #Initialize Web Browser Driver
    browser = webdriver.Firefox()
    element=None
    taskresults=[False,None,False,None,element]

    #print (str(len(taskresults)))
    for vtask in vtesttasks:
        #print (str(len(taskresults)))
        taskresults=executetask(name,browser,vtask,taskresults[4])
        #print (" --> "+str(taskresults[0]))
        if taskresults[0] == False:
            print (" ----> TEST "+ name +" ended not OK on test " + str(vtask))
            break
		
		
    #time.sleep(10)


    browser.quit()

def executetask(name,vbrowser, vtask,velement):
    #print ("TASK --> "+vtask )
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
    #print ("ARG COUNT=> "+ str(len(arguments)))
    while command:
        try:
            if command == "open":
                vbrowser.get(arguments)
                break
            if command == "set_page_load_timeout" :
                vbrowser.set_page_load_timeout(arguments[0])
                break
            if command == "close" :
                #time.sleep(5)
                vbrowser.close()
                break
            if command == "find_element_by_name":
                relement=vbrowser.find_element_by_name(arguments[0])
                #print ("Devolvemos elemento....")
                break
            if command == "find_element_by_id":
                relement=vbrowser.find_element_by_id(arguments[0])
                break
            if command == "find_text_in_source":
                #browser.getPageSource().contains(arguments[0])
                #print ("Devolvemos elemento....")
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
                #print (arguments[0])
                #links = [str(links) for links in vbrowser.find_elements_by_xpath(arguments[0])]
                vbrowser.find_elements_by_xpath(arguments[0])
                #links = vbrowser.find_elements_by_xpath(arguments[0])
                #print (links)
                #for a in links:
                #    print(a.get_attribute('href'))
                break
            if command == "find_test_in_tittle":
                pagetitle=vbrowser.title
                #print (pagetitle)
                if not arguments[0] in pagetitle:
                #    print (" ----->> FOUND "+arguments[0]+" in " + pagetitle)
                #else:
                    rtask=False
                break


            if command == "mytest":
                print ()
                print ("TESTS")
                #price = vbrowser.find_element(By.CSS_SELECTOR, "div[id$='_price']")
                #price.text
                elem = vbrowser.find_element_by_xpath("/html")

                print (vbrowser.title)
                if arguments[0] in vbrowser.title:
                    print (" ----->> FOUND "+arguments[0]+" in " + vbrowser.title)
                    break
                #print(vbrowser.page_source.encode('utf-8', 'ignore'))
                #source_code = elem.get_attribute("outerHTML")
                #print (source_code.encode('utf-8', 'ignore'))
                #vbrowser.get_html_source()
                #vbrowser.is_text_present(arguments[0])
                # print (links)
                # for a in links:
                    # print()
                    # print (a)
                    # print(a.text)
                    # print()
                break


            print ("Command not found")
            rtask=False
            break
            
        except:
            rtask=False
            break
            
    results=[rtask,rtext,rfound,rtimespend,relement]
    return results

def main(argv):

    global debug, tasksfile, starttime, stoptime
    tasksfile=""
    starttime = time.clock()

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
    totaltests=len (testsconfigs)
    count=1
    for name in testsnames:
        print (str(count)+"/"+str(totaltests)+" - "+str(name))
        #print (testsconfigs[name])
        testtasks=testsconfigs[name]
        exectest(name,testtasks)
        count += 1
    stoptime = time.clock()
    executiontime=stoptime-starttime
    print ("All tests execution time: "+ str(executiontime)+" seconds")
    
    
    
    
if __name__ == "__main__":
    main(sys.argv[1:])      
