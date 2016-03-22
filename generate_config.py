#!/usr/bin/python

import os
import json
import sys
				

sourceDir = "./"
bFlag = False



def main():
	jsonReady = []
	toDict = {}
	for root, dirs, files in os.walk(".", topdown=False):
    		for name in sorted(files):
			if ".robot" in name:
        			filePath = os.path.join(root, name)
				
				sp = filePath.split('/')
				sp.remove('.')
				
				if sp[0] not in toDict.keys():
                                        toDict[sp[0]] = {}
                                        sub = toDict[sp[0]]

                                if sp[1] not in sub.keys():
                                        temp = { sp[1] : {} }

				rf = readFile( filePath )
				tc = getTestCasesName( rf )
				
				temp2 = { name : tc }
                                temp[sp[1]].update(temp2)
                                toDict[sp[0]].update(temp)

	jsonReady.append(toDict)		

	writeJsonToFile(json.dumps(jsonReady, sort_keys=True, indent=4))



def writeJsonToFile( dump ):
	orig_stdout = sys.stdout
	f = file('MasterConfig.json', 'w')
	sys.stdout = f

	print dump

	sys.stdout = orig_stdout
	f.close() 



def readFile( path ):
	fo = open(path, "rw+")	
	lines = fo.readlines()
	fo.close()

	return lines



def getTestCasesName( lines ):
	tcIndex = lines.index('*** Test Cases ***\n')
	lines = lines[tcIndex+1:]
	kwIndex = lines.index('*** Keywords ***\n')
	lines = lines[:kwIndex]
	testCases = []

	for line in lines:
		if ( not line.startswith(' ') ):
			if ( line <> '\n'):
				line = line[:-1]
				testCases.append(line)

	return testCases



if __name__ == '__main__':
	main()
