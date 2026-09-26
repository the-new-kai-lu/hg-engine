/* Preserve full approved dex prose using three-line pages in the native window.
 * Only the eleven custom descriptions use paging. Pages advance every 480 menu updates.
 * Addresses below are the US HeartGold overlay-18 routines this engine patches.
 */
#include "types.h"
#include "message.h"
#include "window.h"
#include "constants/species.h"

static String *sPendingDescription;
static struct Window *sDescriptionWindow;
static u16 sDescription[256];
static u16 sLength, sPage, sPageCount, sFrame, sLinesPerPage, sDescriptionSpecies;
static u32 sFont, sColor, sMagic;
static BOOL sPrintedThisFrame;

static void DrawDescriptionPage(void)
{
    struct { u16 maxsize, size; u32 magic; u16 data[256]; } page;
    page.maxsize = 256; page.size = 0; page.magic = sMagic;
    u32 firstLine = sPage * sLinesPerPage, line = 0;
    for (u32 i = 0; i < sLength; i++) {
        if (sDescription[i] == 0xE000) {
            line++;
            if (line > firstLine && line < firstLine + sLinesPerPage)
                page.data[page.size++] = 0xE000;
        } else if (line >= firstLine && line < firstLine + sLinesPerPage) {
            page.data[page.size++] = sDescription[i];
        }
    }
    page.data[page.size] = 0xFFFF;
    FillWindowPixelBuffer(sDescriptionWindow, 0);
    AddTextPrinterParameterizedWithColor(sDescriptionWindow, sFont, (String *)&page,
        4, 0, 0xFF, sColor, NULL);
    ScheduleWindowCopyToVram(sDescriptionWindow);
}

String *FakemonDexDescription(u16 species, int language, int entry, u32 heap)
{
    int message, flag, languageIndex;
    const int banks[] = {810, 805, 806, 807, 808, 809};
    typedef void (*LanguageInfo)(u16, int, int *, int *, int *);
    typedef String *(*ReadEntry)(int, int, u32);
    ((LanguageInfo)0x021E5A51)(species, language, &message, &flag, &languageIndex);
    int bank = languageIndex == 6 ? 803 : banks[languageIndex];
    if (languageIndex == 6) message = species;
    String *result = ((ReadEntry)0x021E5A11)(bank, message + entry, heap);
    sPendingDescription = species >= SPECIES_VOLTUFF && species <= SPECIES_RAGNAROC ? result : NULL;
    sDescriptionWindow = NULL;
    sDescriptionSpecies = species;
    return result;
}

void FakemonDexPrint(struct Window *window, String *str, u32 x, u32 y, u32 font, u32 color, u32 alignment)
{
    if (str != NULL && str == sPendingDescription) {
        sPendingDescription = NULL;
        sDescriptionWindow = window;
        sLength = str->size < 255 ? str->size : 255;
        sMagic = str->magic; sFont = font; sColor = color;
        u32 lines = 1;
        for (u32 i = 0; i < sLength; i++) {
            sDescription[i] = str->data[i];
            if (str->data[i] == 0xE000) lines++;
        }
        sLinesPerPage = window->height / 2;
        if (sLinesPerPage == 0) sLinesPerPage = 1;
        if (sLinesPerPage > 3) sLinesPerPage = 3;
        sPageCount = (lines + sLinesPerPage - 1) / sLinesPerPage;
        sPage = 0; sFrame = 0; sPrintedThisFrame = TRUE;
        DrawDescriptionPage();
        return;
    }
    // Preserve the original text helper for every other dex label and language.
    typedef u32 (*Width)(u8, String *, u32);
    if (alignment == 1) x -= ((Width)0x02002F31)(font, str, 0);
    if (alignment == 2) x -= ((Width)0x02002F31)(font, str, 0) / 2;
    AddTextPrinterParameterizedWithColor(window, font, str, x, y, 0xFF, color, NULL);
}

BOOL FakemonDexMain(void *app, int *state)
{
    typedef int (*Sequence)(void *);
    typedef void (*Update)(void *);
    Sequence const *sequences = (Sequence const *)0x021F9C3C;
    int previous = *state;
    sPrintedThisFrame = FALSE;
    *state = sequences[*state](app);
    // A transition can free windows: invalidate before touching saved pointers.
    if (*state != previous && !sPrintedThisFrame) sDescriptionWindow = NULL;
    if (*state == 93) { sDescriptionWindow = NULL; sPendingDescription = NULL; return FALSE; }
    typedef u16 (*CurrentSpecies)(void *);
    if (sDescriptionWindow != NULL && ((CurrentSpecies)0x021F8839)(app) != sDescriptionSpecies)
        sDescriptionWindow = NULL; // Blank/unseen grid cells may keep the same main state.
    if (sDescriptionWindow != NULL && sPageCount > 1 && ++sFrame >= 480) {
        sFrame = 0; sPage = (sPage + 1) % sPageCount;
        DrawDescriptionPage();
    }
    ((Update)0x02019935)(*(void **)((u8 *)app + 8));
    ((Update)0x021F1005)(app);
    ((Update)0x0200D021)(*(void **)((u8 *)app + 0x66C));
    return TRUE;
}
