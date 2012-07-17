from PySide.QtCore import *
from PySide.QtGui import *
import sys
import re
from random import random

class UnityLogCatApplication(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle('PyLogCat for Unity and Android')

        x, y, w, h = 500, 200, 600, 400
        self.setGeometry(x, y, w, h)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        

        self.mainLayout = QGridLayout()
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.setSpacing(0)

        self.outputArea = QTextEdit(self)
        self.outputArea.setWordWrapMode(QTextOption.NoWrap)
        
        self.mainLayout.addWidget(self.outputArea, 0, 0, 1, 3)


        self.sparklines = {'cpu_player': Sparkline(self, 'cpu-player', ['max','avg','min'], [QColor(200,0,0,255), QColor(0,0,200,255), QColor(0,200,0,255)] ),
                           'cpu_ogles': Sparkline(self, 'cpu-ogles-drv', ['max','avg','min'], [QColor(200,0,0,255), QColor(0,0,200,255), QColor(0,200,0,255)] ),
                           'cpu_present': Sparkline(self, 'cpu-present', ['max','avg','min'], [QColor(200,0,0,255), QColor(0,0,200,255), QColor(0,200,0,255)] ),
                           'frametime': Sparkline(self, 'frametime', ['max','avg','min'], [QColor(200,0,0,255), QColor(0,0,200,255), QColor(0,200,0,255)] , targetVal=33.0),
                           'draw_call': Sparkline(self, 'draw-call #', ['max','avg','min'], [QColor(200,0,0,255), QColor(0,0,200,255), QColor(0,200,0,255)] , targetVal=25.0),
                           'tris': Sparkline(self, 'tris #', ['max','avg','min'], [QColor(200,0,0,255), QColor(0,0,200,255), QColor(0,200,0,255)] ),
                           'verts': Sparkline(self, 'verts #', ['max','avg','min'], [QColor(200,0,0,255), QColor(0,0,200,255), QColor(0,200,0,255)] ),
                           'player_detail': Sparkline(self, 'player-detail', ['physx', 'animation', 'culling', 'skinning', 'batching', 'render'], [QColor(200,0,0,255), QColor(200,200,0,255), QColor(0,200,0,255), QColor(0,200,200,255), QColor(0,0,200,255), QColor(200,0,200,255)], stacked=True ),
                           'fixed_update_count': Sparkline(self, 'fixed-update-count', ['max', 'min']),
                           'mono_scripts': Sparkline(self, 'mono-scripts', ['update', 'fixedUpdate', 'coroutines'], [QColor(200,0,0,255), QColor(0,200,0,255), QColor(0,0,200,255)], stacked=True),
                           'mono_memory': Sparkline(self, 'mono-memory', ['used', 'allocated']),
                           'collections': Sparkline(self, 'collections', ['']),
                           'collection_duration': Sparkline(self, 'collection-duration', [''])
                          }

        self.mainLayout.addWidget(self.sparklines['cpu_player'], 1, 0);
        self.mainLayout.addWidget(self.sparklines['cpu_ogles'], 1, 1);
        self.mainLayout.addWidget(self.sparklines['cpu_present'], 1, 2);
        
        self.mainLayout.addWidget(self.sparklines['frametime'], 2, 0);
        
        self.mainLayout.addWidget(self.sparklines['draw_call'], 3, 0);
        self.mainLayout.addWidget(self.sparklines['tris'], 3, 1);
        self.mainLayout.addWidget(self.sparklines['verts'], 3, 2);
        
        self.mainLayout.addWidget(self.sparklines['player_detail'], 4, 0);
        self.mainLayout.addWidget(self.sparklines['fixed_update_count'], 4, 1);
        self.mainLayout.addWidget(self.sparklines['mono_scripts'], 4, 2);
        
        self.mainLayout.addWidget(self.sparklines['mono_memory'], 5, 0);
        self.mainLayout.addWidget(self.sparklines['collections'], 5, 1);
        self.mainLayout.addWidget(self.sparklines['collection_duration'], 5, 2);

        self.monitor = OutputMonitor(self)
        self.mainLayout.addWidget(self.monitor, 6, 0, 1, 3)

        self.setLayout(self.mainLayout)



        self.command = CommandExecutor(self, r'C:\Program Files\Android\android-sdk\platform-tools\adb.exe', ['logcat', 'Unity:V'], self.parseOutput)

        self.command.execute()
    
    def closeEvent(self, event):
        self.command.kill()

        event.accept()

    def parseOutput(self, output):

        self.monitor.gotConnection()

        lines = output.split('\n')
        for line in lines:
            match = re.match(r'D/Unity\s*\(\s*\d*\s*\):\s*cpu-player>\s*min:\s*(?P<min>[0-9.]*)\s*max:\s*(?P<max>[0-9.]*)\s*avg:\s*(?P<avg>[0-9.]*)', line)
            if match:
                self.sparklines['cpu_player'].updateData( [float( match.group('max') ), float( match.group('avg') ), float( match.group('min') )] )
                continue

            match = re.match(r'D/Unity\s*\(\s*\d*\s*\):\s*cpu-ogles-drv>\s*min:\s*(?P<min>[0-9.]*)\s*max:\s*(?P<max>[0-9.]*)\s*avg:\s*(?P<avg>[0-9.]*)', line)
            if match:
                self.sparklines['cpu_ogles'].updateData( [float( match.group('max') ), float( match.group('avg') ), float( match.group('min') )] )
                continue

            match = re.match(r'D/Unity\s*\(\s*\d*\s*\):\s*cpu-present>\s*min:\s*(?P<min>[0-9.]*)\s*max:\s*(?P<max>[0-9.]*)\s*avg:\s*(?P<avg>[0-9.]*)', line)
            if match:
                self.sparklines['cpu_present'].updateData( [float( match.group('max') ), float( match.group('avg') ), float( match.group('min') )] )
                continue

            match = re.match(r'D/Unity\s*\(\s*\d*\s*\):\s*frametime>\s*min:\s*(?P<min>[0-9.]*)\s*max:\s*(?P<max>[0-9.]*)\s*avg:\s*(?P<avg>[0-9.]*)', line)
            if match:
                self.sparklines['frametime'].updateData( [float( match.group('max') ), float( match.group('avg') ), float( match.group('min') )] )
                continue

            match = re.match(r'D/Unity\s*\(\s*\d*\s*\):\s*draw-call #>\s*min:\s*(?P<min>[0-9.]*)\s*max:\s*(?P<max>[0-9.]*)\s*avg:\s*(?P<avg>[0-9.]*)', line)
            if match:
                self.sparklines['draw_call'].updateData( [float( match.group('max') ), float( match.group('avg') ), float( match.group('min') )] )
                continue

            match = re.match(r'D/Unity\s*\(\s*\d*\s*\):\s*tris #>\s*min:\s*(?P<min>[0-9.]*)\s*max:\s*(?P<max>[0-9.]*)\s*avg:\s*(?P<avg>[0-9.]*)', line)
            if match:
                self.sparklines['tris'].updateData( [float( match.group('max') ), float( match.group('avg') ), float( match.group('min') )] )
                continue

            match = re.match(r'D/Unity\s*\(\s*\d*\s*\):\s*verts #>\s*min:\s*(?P<min>[0-9.]*)\s*max:\s*(?P<max>[0-9.]*)\s*avg:\s*(?P<avg>[0-9.]*)', line)
            if match:
                self.sparklines['verts'].updateData( [float( match.group('max') ), float( match.group('avg') ), float( match.group('min') )] )
                continue

            match = re.match(r'D/Unity\s*\(\s*\d*\s*\):\s*player-detail>\s*physx:\s*(?P<physx>[0-9.]*)\s*animation:\s*(?P<animation>[0-9.]*)\s*culling\s*(?P<culling>[0-9.]*)\s*skinning:\s*(?P<skinning>[0-9.]*)\s*batching:\s*(?P<batching>[0-9.]*)\s*render:\s*-?(?P<render>[0-9.]*)\s*fixed-update-count:\s*(?P<fixed_update_min>[0-9.]*)\s*\.\.\s*(?P<fixed_update_max>[0-9.]*)', line)
            if match:
                self.sparklines['player_detail'].updateData( [float( match.group('physx') ), float( match.group('animation') ), float( match.group('culling') ), float( match.group('skinning') ), float( match.group('batching') ), float( match.group('render') )] )
                self.sparklines['fixed_update_count'].updateData( [float( match.group('fixed_update_max') ), float( match.group('fixed_update_min') )] )
                continue

            match = re.match(r'D/Unity\s*\(\s*\d*\s*\):\s*mono-scripts>\s*update:\s*(?P<update>[0-9.]*)\s*fixedUpdate:\s*(?P<fixedUpdate>[0-9.]*)\s*coroutines:\s*(?P<coroutines>[0-9.]*)', line)
            if match:
                self.sparklines['mono_scripts'].updateData( [float( match.group('update') ), float( match.group('fixedUpdate') ), float( match.group('coroutines') )] )
                continue

            match = re.match(r'D/Unity\s*\(\s*\d*\s*\):\s*mono-memory>\s*used heap:\s*(?P<used>[0-9.]*)\s*allocated heap:\s*(?P<allocated>[0-9.]*)\s*max number of collections:\s*(?P<maxCollections>[0-9.]*)\s*collection total duration:\s*(?P<collectionDuration>[0-9.]*)', line)
            if match:
                self.sparklines['mono_memory'].updateData( [float( match.group('used') ), float( match.group('allocated') ) ] )
                self.sparklines['collections'].updateData( [float( match.group('maxCollections') )] )
                self.sparklines['collection_duration'].updateData( [float( match.group('collectionDuration') )] )
                continue

            # Discard these lines, they are known to be useless:
            match = re.match(r'D/Unity\s*\(\s*\d*\s*\): Android Unity', line)
            if match:
                continue

            match = re.match(r'D/Unity\s*\(\s*\d*\s*\): ------', line)
            if match:
                continue

            # Not matched by anything else, so print to the log
            match = re.match(r'./Unity', line)
            if match:
                self.outputArea.moveCursor(QTextCursor.End)
                self.outputArea.insertPlainText(line.rstrip()+'\n') #exactly one newline, please
                continue




class OutputMonitor(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.connectionLost)
        self.timer.setSingleShot(True)

        self.setMinimumSize(20,20)
        self.setMaximumSize(20,20)

    def gotConnection(self):
        self.timer.start(5000)
        self.update()

    def connectionLost(self):
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter()

        painter.begin(self)

        minDim = min( self.width(), self.height)

        if self.timer.isActive():
            painter.setBrush(QBrush(QColor(0,255,0,255),Qt.SolidPattern))
        else:
            painter.setBrush(QBrush(QColor(255,0,0,255),Qt.SolidPattern))
        
        painter.drawEllipse( QRect(3,3,self.width()-6,self.height()-6 ) )

        painter.end()

class Sparkline(QWidget):
    def __init__(self, parent, name, entries, colors=None, targetVal=-1, targetColor=None, stacked=False):
        QWidget.__init__(self, parent)

        # tooltips
        self.setMouseTracking(True)
        
        self.entries = entries if entries else ['']
        
        self.colors = colors if colors is not None else [QColor(0,0,0,64)] * len(self.entries)
        self.targetVal = targetVal
        self.targetColor = targetColor if targetColor is not None else QColor(255,255,255,128)

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)

        self.header = QLabel()
        self.header.setText(name)
        self.layout.addWidget(self.header, 0, 0, 1, 2)

        self.graph = Graph(self, self.colors, self.targetVal, self.targetColor, stacked)
        self.layout.addWidget(self.graph, 1, 0, len( self.entries ), 1)

        self.labels = []
        for i,e in enumerate(self.entries):
            label = QLabel()
            label.setText(e)
            label.setPalette( QPalette( text=QBrush( color=self.colors[i], bs=Qt.SolidPattern ) ) )
            self.layout.addWidget(label, i+1, 1)
            self.labels.append(label)

        self.setLayout(self.layout)

        self.focused = False


    def setLabels(self, entries, data):
        for i,(e,d) in enumerate(zip(entries, data)):
            self.labels[i].setText( str(d) + ' ' + e )

    def updateData(self, data):
        self.graph.updateData(data)
        
        if not self.focused:
            self.setLabels(self.entries, data)


    def mouseMoveEvent(self, event):
        self.mousePressEvent(event)

    def mousePressEvent(self, event):
        if self.graph.geometry().contains( event.pos() ):
            data = self.graph.getDataForPosition(event.pos())
            dataText = '\n'.join( [ ': '.join(z) for z in zip(self.entries, map(str,data)) ] )
            self.setLabels(self.entries, data)
            self.focused = True
        else:
            self.graph.hideDataForPosition()
            self.focused = False

        self.graph.update()


class Graph(QWidget):
    def __init__(self, parent, colors, targetVal, targetColor, stacked=False):
        QWidget.__init__(self, parent)

        self.colors = colors
        self.targetVal = targetVal
        self.targetColor = targetColor

        self.stacked = stacked

        self.dataHistory = []

        self.setMinimumSize(70,20)
        self.setMaximumSize(150,100)

        self.sw = 2 #slice width
        self.highlightIndex = -1

    def updateData(self, data):
        self.dataHistory.append(data)
        
        self.update()

    def getDataForPosition(self, parentPosition):
        localPos = parentPosition - self.pos()

        rightIndex = (self.width()-localPos.x()) / self.sw
        absIndex = len(self.dataHistory)-rightIndex

        absIndex = max(0, min(absIndex, len(self.dataHistory)-1) )
        self.highlightIndex = absIndex
        return self.dataHistory[absIndex]
    
    def hideDataForPosition(self):
        self.highlightIndex = -1

    def paintEvent(self, event):
        painter = QPainter()

        sw = self.sw
        
        rightIndex = (self.width()/sw)+2
        rightIndex = min(rightIndex, len(self.dataHistory)-1)
        dataSlice = self.dataHistory[-rightIndex:]

        length = len(dataSlice)*sw
        
        maxDataIndex = -1
        maxData = max(self.targetVal,1)
        secondMaxData = max(self.targetVal,1)
        for i,s in enumerate(dataSlice):
            if self.stacked:
                stackSum = 0
                for d in s:
                    stackSum += d
                if stackSum > maxData:
                    secondMaxData = maxData
                    maxData = stackSum
                    maxDataIndex = i
                elif stackSum > secondMaxData:
                    secondMaxData = stackSum
            else:
                for d in s:
                    if d > maxData:
                        secondMaxData = maxData
                        maxData = d
                        maxDataIndex = i
                    elif d > secondMaxData:
                        secondMaxData = d

        painter.begin(self)
        
        painter.setPen(QPen(QColor(0,0,0,255), 1))
        painter.drawRect(0,0,self.width()-1, self.height()-1)

        for i,d in enumerate(dataSlice):

            if self.stacked:
                stackTop = 0

            for num in range( len(d) ):
                
                if i == maxDataIndex:
                    painter.setPen(QPen(QColor(255,255,0,255), sw))
                else:
                    painter.setPen(QPen(self.colors[num], sw))
                
                if self.highlightIndex >= 0 and len(self.dataHistory)-rightIndex+i != self.highlightIndex:
                    faded = painter.pen().color()
                    faded.setAlpha(faded.alpha()/4)
                    painter.setPen(QPen(faded, sw))

                if self.stacked:
                    painter.drawLine( (self.width()-1-length)+(i*sw),
                        self.height()-1-((self.height()-2)*(stackTop/secondMaxData)),
                        (self.width()-1-length)+(i*sw),
                        self.height()-1-((self.height()-2)*((d[num]+stackTop)/secondMaxData)) )
                    stackTop += d[num]
                else:
                    painter.drawLine( (self.width()-1-length)+(i*sw),
                        self.height()-1,
                        (self.width()-1-length)+(i*sw),
                        self.height()-1-((self.height()-2)*(d[num]/secondMaxData)) )
                
                #if len(self.dataHistory)-rightIndex+i == self.highlightIndex:
                    #painter.setPen(QPen(QColor(255,255,255,128), sw))
                    #painter.drawLine( (self.width()-1-length)+(i*sw),
                        #0,
                        #(self.width()-1-length)+(i*sw),
                        #self.height()-1 )

        if self.targetVal >= 0:
            painter.setPen(QPen(self.targetColor, 1))
            painter.drawLine(0,
                    self.height()-1-((self.height()-2)*(self.targetVal/secondMaxData)),
                    self.width(),
                    self.height()-1-((self.height()-2)*(self.targetVal/secondMaxData)) )

        painter.end()

class CommandExecutor:
    def __init__(self, parent, command, argList, outputFunction):
        self.command = command
        self.argList = argList
        self.outputFunction = outputFunction

        print ('preparing process ' + command)

        self.process = QProcess(parent)
        self.process.readyReadStandardOutput.connect(self.read_output)
        self.process.readyReadStandardError.connect(self.read_error)
        self.process.started.connect(self.started)
        self.process.finished.connect(self.finished)


    def execute(self):
        print ('executing!')
        self.process.start(self.command, self.argList)

    def started(self):
        print ('started!')

    def read_output(self):
        self.outputFunction( str( self.process.readAllStandardOutput() ) )

    def read_error(self):
        print ('error!')
        self.outputFunction( 'ERROR - - - -\n\n ' + str( self.process.readAllStandardOutput() ) )

    def finished(self, errorCode):
        print ('********* finished!')
        self.outputFunction( "\n--FINISHED--" )

    def kill(self):
        self.process.kill()


if __name__ == '__main__':
    root = QApplication(sys.argv)
    window = UnityLogCatApplication()
    window.show()
    window.raise_()

    sys.exit(root.exec_())
