#!/usr/bin/env python
# coding: utf-8

# ### xls 형식 xlsx 형식으로 변환

# https://ko.extendoffice.com/documents/excel/1349-excel-batch-convert-xls-to-xlsx.html

# In[ ]:


alt + F11 >> visual basic 창 띄우기
우클릭 > 모듈 만들기


# In[ ]:


Sub ConvertToXlsx()
'Updateby Extendoffice
Dim strPath As String
Dim strFile As String
Dim xWbk As Workbook
Dim xSFD, xRFD As FileDialog
Dim xSPath As String
Dim xRPath As String
Set xSFD = Application.FileDialog(msoFileDialogFolderPicker)
With xSFD
.Title = "Please select the folder contains the xls files:"
.InitialFileName = "C:\"
End With
If xSFD.Show <> -1 Then Exit Sub
xSPath = xSFD.SelectedItems.Item(1)
Set xRFD = Application.FileDialog(msoFileDialogFolderPicker)
With xRFD
.Title = "Please select a folder for outputting the new files:"
.InitialFileName = "C:\"
End With
If xRFD.Show <> -1 Then Exit Sub
xRPath = xRFD.SelectedItems.Item(1) & "\"
strPath = xSPath & "\"
strFile = Dir(strPath & "*.xls")
Application.ScreenUpdating = False
Application.DisplayAlerts = False
Do While strFile <> ""
If Right(strFile, 3) = "xls" Then
Set xWbk = Workbooks.Open(Filename:=strPath & strFile)
xWbk.SaveAs Filename:=xRPath & strFile & "x", _
FileFormat:=xlOpenXMLWorkbook
xWbk.Close SaveChanges:=False
End If
strFile = Dir
Loop
Application.DisplayAlerts = True
Application.ScreenUpdating = True
End Sub



# excel로 돌아가서 개발도구 >> 매크로기록
# F5 >> 실행
# xls 파일 저장 폴더 선택
# xlsx 파일 저장할 폴더 선택
# 실행!
