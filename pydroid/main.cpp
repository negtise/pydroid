#include <Python.h>
#include <stdio.h>
#include <android/log.h>
#include <binder/ProcessState.h>

//void initandroidembed();
extern "C"
{
void initbinder_();
void initmediaplayer_();
void initandroidlog();
void init_io(void);
//void initmain(void);
void initserver();

}

void initPyDroid()
{
//    initandroidembed();
    initbinder_();  
    initmediaplayer_();  
}

extern "C" void pydroid_init()
{
    static int bInit=0;
    if(bInit) return;
    PyEval_InitThreads();
	android::ProcessState::self()->startThreadPool();
    bInit = 1;
}

extern "C" int pydroid_main(int argc,char *argv[])
{
    printf("+++++++++++argc %d \n",argc);

    Py_InitializeEx(0);
    PyEval_InitThreads();
    
    initPyDroid();

    initandroidlog();

	android::ProcessState::self()->startThreadPool();


/*
    PyRun_SimpleString(
        "import sys, posix\n" \
        "import androidlog\n" \
        "class LogFile(object):\n" \
        "    def __init__(self):\n" \
        "        self.buffer = ''\n" \
        "    def write(self, s):\n" \
        "        s = self.buffer + s\n" \
        "        lines = s.split(\"\\n\")\n" \
        "        for l in lines[:-1]:\n" \
        "            pylog.i(l)\n" \
        "        self.buffer = lines[-1]\n" \
        "    def flush(self):\n" \
        "        return\n" \
        "sys.stdout = sys.stderr = LogFile()\n");
*/
    
    if(argc <= 1)
    {
        return PyRun_SimpleString(
            "import main\n" \
            "main.run()\n"
            );
    }
    else
    {
        return Py_Main(argc,argv);
    }
}
