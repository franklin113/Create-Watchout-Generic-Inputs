#duplicateInputs: accepts user input and duplicates watchout generic inputs.
#user input is stored so it can operate with little input

import pyperclip, sys, shelve

def get_text():
	exampleText = '''UTF8 DATATON_DFC_DATA_590925_620721_AUC069 {
	"Structure and File Format (C) Copyright Dataton AB" 2016 1
	"WATCHMAKER" 6 1 1 0
	ObjTransferable ObjTransferable struct extends {
		TextTransferable struct extends {
			Transferable struct {
			}
		} {
		}
	} {
		mObjData list object true,
		mClassName string
	} {
		{ // mObjData
			InternalVariable struct extends {
				Variable struct extends {
					VarListItem struct {
						mName string
					}
				} {
					mValue variant,
					mLimit float
				}
			} {
			} { "%s %s", %s, %s // mName mValue mLimit
			},
		},
		"VarListItem" // mClassName
	}
}

	'''
	return exampleText

#			} { "%s -%s", %s, %s // mName mValue mLimit

def build_clipboard(userList):
	#1 header
	#2 count
	#3 start num
	#4 value
	#5 limit

	woData = get_text() % (userList[0],userList[2],userList[3], userList[4])
	splitData = woData.splitlines()
	curLine = 26
	for i in range(1, int(userList[1])+1):
		curNum = i
		lineBuilder = '			InternalVariable { "%s %d", %s, %s } // mName mValue mLimit' % (userList[0],curNum + int(userList[2]),userList[3],userList[4])


		splitData.insert(curLine,lineBuilder)

		# curLine += 1
	return '\n'.join(splitData)

def get_user():
	'''
	Retriever user input here
	The options are - prefix, count, startNumber, value, limit
	:return: list: [headerName,count,startNum, value, limit]
	'''

	### Wrote this a couple years ago when I didn't know how to do this more efficiently.. 
	#todo - clean this garbage up
	store = shelve.open('DuplicateInputData')

	if len(sys.argv) == 1:
		headerName = store['headerName']
		count = store['count']
		startNum = store['startNum']
		value = store['value']
		limit = store['limit']

	#assign values accross the board here
	elif len(sys.argv) > 0 and len(sys.argv) < 3:
		headerName = sys.argv[1]
		count = store['count']
		startNum = store['startNum']
		value = store['value']
		limit = store['limit']


	elif len(sys.argv) == 3:
		headerName = sys.argv[1]
		count = sys.argv[2]
		startNum = store['startNum']
		value = store['value']
		limit = store['limit']

	elif len(sys.argv) == 4:
		headerName = sys.argv[1]
		count = sys.argv[2]
		startNum = sys.argv[3]
		value = store['value']
		limit = store['limit']

	elif len(sys.argv) == 5:
		headerName = sys.argv[1]
		count = sys.argv[2]
		startNum = sys.argv[3]
		value = sys.argv[4]
		limit = store['limit']

	elif len(sys.argv) == 6:
		#This all has to be run at least once
		headerName = sys.argv[1]
		count = sys.argv[2]
		startNum = sys.argv[3]
		value = sys.argv[4]
		limit = sys.argv[5]

		#save all these as default
		store['headerName'] = headerName
		store['count'] = count
		store['startNum'] = startNum
		store['value'] = value
		store['limit'] = limit

	store.close()
	return [headerName,count,startNum, value, limit]

newData = build_clipboard(get_user())
pyperclip.copy(newData)