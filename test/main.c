#include <stdio.h>
#include <Python.h>
extern int pydroid_main(int argc,char *argv[]);

#if 0
void SDLSurfaceView_nativeInit()
{
    int argc = 1;  
    char * argv[] = { "sdl" };  
    SDL_main(argc,argv);
}
#endif

int main(int argc,char *argv[])
{
//    SDLSurfaceView_nativeInit();
//    return pydroid_main(argc,argv);
    return Py_Main(argc,argv);
}
