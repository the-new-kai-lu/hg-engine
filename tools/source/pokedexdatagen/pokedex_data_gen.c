#include <stdio.h>
#include <stdlib.h>

#include "../../../include/pokedex_archive_data.h"

static int Streq(const char *lhs, const char *rhs) {
    while (*lhs != '\0' && *lhs == *rhs) {
        lhs++;
        rhs++;
    }

    return *lhs == *rhs;
}

static int WriteFile(const char *path, const void *data, size_t size) {
    FILE *fp = fopen(path, "wb");

    if (fp == NULL) {
        perror(path);
        return 1;
    }

    if (size != 0 && fwrite(data, 1, size, fp) != size) {
        perror(path);
        fclose(fp);
        return 1;
    }

    if (fclose(fp) != 0) {
        perror(path);
        return 1;
    }

    return 0;
}

static int WritePokedexSortArchive(const char *outDir) {
    char path[512];
    u32 member, count = sPokedexSortListCount;

    for (member = 0; member < count; member++) {
        const PokedexU16List *list = &sPokedexSortLists[member];

        snprintf(path, sizeof(path), "%s/%03u.bin", outDir, member + POKEDEX_SORT_FIXED_MEMBER_COUNT);
        if (WriteFile(path, list->data, list->count * sizeof(*list->data)) != 0) {
            return 1;
        }
    }

    return 0;
}

static int WritePokedexAreaArchive(const char *outDir) {
    char path[512];
    u32 member = 0;
    u32 baseCount = sPokedexAreaBaseMemberCount;
    u32 listCount = sPokedexAreaListCount;

    for (; member < baseCount; member++) {
        const PokedexArchiveMember *baseMember = &sPokedexAreaBaseMembers[member];
        snprintf(path, sizeof(path), "%s/0_a133_%04u", outDir, member);
        if (WriteFile(path, baseMember->data, baseMember->size) != 0) {
            return 1;
        }
    }

    /* The legacy source contains eight groups, then one unused member.
     * Expand each group independently: simply appending new species would
     * shift day/night lookups into another species' locations. Include slot
     * zero and the final species, which the old 1075-wide groups omitted. */
    const u32 oldStride = (listCount - 1) / 8;
    const u32 newStride = SPECIES_MAX_MON_NUM + 1;
    const u32 unknownArea = 0;
    for (; member < baseCount + 8 * newStride + 1; member++) {
        u32 index = member - baseCount;
        u32 group = index / newStride;
        u32 species = index % newStride;
        const void *data = &unknownArea;
        size_t size = sizeof(unknownArea);
        if (group < 8 && species < oldStride) {
            const PokedexU32List *list = &sPokedexAreaLists[group * oldStride + species];
            data = list->data;
            size = list->count * sizeof(*list->data);
        }
        snprintf(path, sizeof(path), "%s/3_%04u", outDir, member);
        if (WriteFile(path, data, size) != 0) return 1;
    }

    return 0;
}

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "usage: %s <a214|a133> <outdir>\n", argv[0]);
        return 1;
    }

    if (Streq(argv[1], "a214")) {
        return WritePokedexSortArchive(argv[2]);
    }

    if (Streq(argv[1], "a133")) {
        return WritePokedexAreaArchive(argv[2]);
    }

    fprintf(stderr, "unknown archive kind: %s\n", argv[1]);
    return 1;
}
