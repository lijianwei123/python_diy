#encoding: utf-8
'''
Created on 2013-12-16

@author: Administrator
'''
import wx
import os
import urllib


class FindFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "找回电脑", size=(300, 300))
        self.panel1 = wx.Panel(self, -1)
        self.btn1 = wx.Button(self.panel1, -1, "开始", pos = (100, 20))
        self.btn2 = wx.Button(self.panel1, -1, "停止", pos = (100, 50))
    
        
        #绑定事件
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.btn1)
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.btn2)
        
    def OnClick(self, event):
        #self.btn1.SetLabel("停止")
        btn_label = event.GetEventObject().GetLabel()
        if (btn_label == '开始'):
            print self.requestIp()
        elif (btn_label == '停止'):
            print 2
            
    def  requestIp(self):
        return urllib.urlopen("http://localhost/test10.php").readline()
    
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = FindFrame()
    frame.Show(True)
    app.MainLoop()