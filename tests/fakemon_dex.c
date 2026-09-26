/* Host tests for complete, unclipped multi-page dex descriptions. */
#include "host_compat.h"
#include "../src/pokedex/fakemon_entries.c"
extern int printf(const char *, ...);
static u16 captured[256];
static u16 capturedSize;
static int failure;
u8 AddTextPrinterParameterizedWithColor(void *window, u8 font, String *text, u32 x, u32 y, u32 speed, u32 color, void *callback) {
    (void)font;(void)x;(void)y;(void)speed;(void)color;(void)callback;
    struct Window *w=window;
    unsigned lines=1;
    capturedSize=text->size;
    for(unsigned i=0;i<text->size;i++) {captured[i]=text->data[i];if(captured[i]==0xE000)lines++;}
    if(lines*16>w->height*8)failure=1;
    if(text->data[text->size]!=0xFFFF)failure=1;
    return 0;
}
void FillWindowPixelBuffer(void *window,u8 fill) {(void)window;(void)fill;}
void ScheduleWindowCopyToVram(struct Window *window) {(void)window;}
int main(void) {
    struct {u16 maxsize,size;u32 magic;u16 data[256];} text={256,0,0xB6F8D2EC,{0}};
    struct Window window={0};
    unsigned checks=0;
    // Distinct characters on each line expose omissions and duplicated page boundaries.
    for(unsigned lines=4;lines<=9;lines++) for(unsigned height=2;height<=8;height+=2) {
        text.size=0;window.height=height;window.width=28;
        for(unsigned line=0;line<lines;line++) {
            if(line)text.data[text.size++]=0xE000;
            for(unsigned j=0;j<24;j++)text.data[text.size++]=100+line;
        }
        text.data[text.size]=0xFFFF;
        sPendingDescription=(String*)&text;
        FakemonDexPrint(&window,(String*)&text,0,0,0,0x20100,0);
        unsigned read=0;
        for(unsigned page=0;page<sPageCount;page++) {
            if(page){if(text.data[read++]!=0xE000)return 2;sPage=page;DrawDescriptionPage();}
            for(unsigned i=0;i<capturedSize;i++)if(captured[i]!=text.data[read++])return 3;
        }
        if(read!=text.size || failure)return 4;
        checks++;
    }
    printf("PASS %u dex paging cases: complete text, correct boundaries, fits native window\n",checks);
    return 0;
}
