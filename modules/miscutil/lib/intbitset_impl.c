// $Id$

// This file is part of Invenio.
// Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010 CERN.
//
// Invenio is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License as
// published by the Free Software Foundation; either version 2 of the
// License, or (at your option) any later version.
//
// Invenio is distributed in the hope that it will be useful, but
// WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
// General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Invenio; if not, write to the Free Software Foundation, Inc.,
// 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.


#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "intbitset.h"

const int wordbytesize = sizeof(word_t);
const int wordbitsize = sizeof(word_t) * 8;

const int maxelem = INT_MAX;

IntBitSet *intBitSetCreate(register const int size, const bool_t trailing_bits) {
    register word_t *base;
    register word_t *end;
    IntBitSet *ret = malloc(sizeof(IntBitSet));
    // At least one word -> the one who represent the trailing_bits
    ret->allocated = (size / wordbitsize + 1);
    ret->size = 0; // trailing_bits
    ret->trailing_bits = trailing_bits ? (word_t) ~0 : 0;
    if (trailing_bits) {
        base = ret->bitset = malloc(ret->allocated * wordbytesize);
        end = base + ret->allocated;
        for (; base < end; ++base)
            *base = (word_t) ~0;
        ret->tot = -1;
    } else {
        ret->bitset = calloc(ret->allocated, wordbytesize);
        ret->tot = 0;
    }
    return ret;
}

IntBitSet *intBitSetCreateNoAllocate() {
    IntBitSet *ret = malloc(sizeof(IntBitSet));
    ret->allocated = 0;
    ret->size = -1;
    ret->trailing_bits = 0;
    ret->bitset = NULL;
    return ret;
}

IntBitSet *intBitSetResetFromBuffer(IntBitSet *const bitset, const void *const buf, const Py_ssize_t bufsize) {
    bitset->allocated = bufsize/wordbytesize;
    free(bitset->bitset);
    bitset->bitset = malloc(bufsize);
    bitset->tot = -1;
    bitset->size = bitset->allocated - 1;
    memcpy(bitset->bitset, buf, bufsize);
    bitset->trailing_bits = *(bitset->bitset + bitset->allocated - 1) ? (word_t) ~0 : 0;
    return bitset;
}

IntBitSet *intBitSetReset(IntBitSet *const bitset) {
    bitset->allocated = 1;
    bitset->size = 0;
    *bitset->bitset = 0;
    bitset->trailing_bits = 0;
    return bitset;
}


IntBitSet *intBitSetCreateFromBuffer(const void *const buf, const Py_ssize_t bufsize) {
    IntBitSet *ret = malloc(sizeof(IntBitSet));
    ret->allocated = bufsize/wordbytesize;
    ret->bitset = malloc(bufsize);
    ret->size = ret->allocated - 1;;
    ret->tot = -1;
    memcpy(ret->bitset, buf, bufsize);
    ret->trailing_bits = *(ret->bitset + ret->allocated - 1) ? (word_t) ~0 : 0;
    return ret;
}


void intBitSetDestroy(IntBitSet *const bitset) {
    free(bitset->bitset);
    free(bitset);
}

IntBitSet *intBitSetClone(const IntBitSet * const bitset) {
    IntBitSet *ret = malloc(sizeof(IntBitSet));
    ret->size = bitset->size;
    ret->tot = bitset->tot;
    ret->trailing_bits = bitset->trailing_bits;
    ret->allocated = bitset->allocated;
    ret->bitset = malloc(bitset->allocated * wordbytesize);
    memcpy(ret->bitset, bitset->bitset, bitset->allocated * wordbytesize);
    return ret;
}

int intBitSetGetSize(IntBitSet * const bitset) {
    register word_t *base;
    register word_t *end;
    if (bitset->size >= 0)
        return bitset->size;
    base = bitset->bitset;
    end = bitset->bitset + bitset->allocated - 2;
    for (; base < end && *end == bitset->trailing_bits; --end);
    bitset->size = ((int) (end - base) + 1);
    return bitset->size;
}

int intBitSetGetTot(IntBitSet *const bitset) {
    register word_t* base;
    register int i;
    register int tot;
    register word_t *end;
    if (bitset->trailing_bits)
        return -1;
    if (bitset->tot < 0) {
        end = bitset->bitset + bitset->allocated;
        tot = 0;
        for (base = bitset->bitset; base < end; ++base)
            if (*base)
                for (i=0; i<wordbitsize; ++i)
                    if ((*base & ((word_t) 1 << i)) != 0) {
                        ++tot;
                    }
        bitset->tot = tot;
    }
    return bitset->tot;
}

int intBitSetGetAllocated(const IntBitSet * const bitset) {
    return bitset->allocated;
}

void intBitSetResize(IntBitSet *const bitset, register const int allocated) {
    register word_t *base;
    register word_t *end;
    if (allocated > bitset->allocated) {
        bitset->bitset = realloc(bitset->bitset, allocated * wordbytesize);
        base = bitset->bitset + bitset->allocated;
        end = bitset->bitset + allocated;
        for (; base<end; ++base)
            *(base) = bitset->trailing_bits;
        bitset->allocated = allocated;
    }
}

bool_t intBitSetIsInElem(const IntBitSet * const bitset, register const int elem) {
    return ((elem < bitset->allocated * wordbitsize) ?
            (bitset->bitset[elem / wordbitsize] & ((word_t) 1 << ((word_t)elem % (word_t)wordbitsize))) != 0 : bitset->trailing_bits != 0);
}

void intBitSetAddElem(IntBitSet *const bitset, register const int elem) {
    if (elem >= (bitset->allocated - 1) * wordbitsize) {
        if (bitset->trailing_bits)
            return;
        else
            intBitSetResize(bitset, (elem + elem/10)/wordbitsize+2);
    }
    bitset->bitset[elem / wordbitsize] |= ((word_t) 1 << (elem % wordbitsize));
    bitset->tot = -1;
    bitset->size = -1;
}

void intBitSetDelElem(IntBitSet *const bitset, register const int elem) {
    if (elem >= (bitset->allocated - 1) * wordbitsize) {
        if (!bitset->trailing_bits)
            return;
        else
            intBitSetResize(bitset, (elem + elem/10)/wordbitsize+2);
    }
    bitset->bitset[elem / wordbitsize] &= (word_t) ~((word_t) 1 << (elem % wordbitsize));
    bitset->tot = -1;
    bitset->size = -1;
}

bool_t intBitSetEmpty(const IntBitSet *const bitset) {
    register word_t *end;
    register word_t *base;
    if (bitset->trailing_bits) return 0;
    if (bitset->tot == 0) return 1;
    end = bitset->bitset + bitset->allocated;
    for (base = bitset->bitset; base < end; ++base)
        if (*base) return 0;
    return 1;
}

int intBitSetAdaptMax(IntBitSet *const x, IntBitSet *const y) {
    // Good idea but broken, it is kept for better time...
    // register int sizex = intBitSetGetSize(x);
    // register int sizey = intBitSetGetSize(y);
    // register int sizemax = ((sizex > sizey) ? sizex : sizey) + 1;
    // if (sizemax > x->allocated)
    //     intBitSetResize(x, sizemax);
    // if (sizemax > y->allocated)
    //     intBitSetResize(y, sizemax);
    // return sizemax;*/
    register int allocated = (x->allocated > y->allocated) ? x->allocated : y->allocated;
    if (allocated > x->allocated)
        intBitSetResize(x, allocated);
    if (allocated > y->allocated)
        intBitSetResize(y, allocated);
    return allocated;
}

int intBitSetAdaptMin(IntBitSet *const x, IntBitSet *const y) {
    register int sizex;
    register int sizey;
    if (x->trailing_bits || y->trailing_bits)
        return intBitSetAdaptMax(x, y);
    sizex = intBitSetGetSize(x);
    sizey = intBitSetGetSize(y);
    return ((sizex < sizey) ? sizex : sizey) + 1;
}

IntBitSet *intBitSetUnion(IntBitSet *const x, IntBitSet *const y) {
    register word_t *xbase;
    register word_t *xend;
    register word_t *ybase;
    register word_t *retbase;
    register IntBitSet * ret = malloc(sizeof (IntBitSet));
    ret->allocated = intBitSetAdaptMax(x, y);
    xbase = x->bitset;
    xend = x->bitset+ret->allocated;
    ybase = y->bitset;
    retbase = ret->bitset = malloc(wordbytesize * ret->allocated);
    ret->size = -1;
    ret->tot = -1;
    for (; xbase < xend; ++xbase, ++ybase, ++retbase)
        *(retbase) = *(xbase) | *(ybase);
    ret->trailing_bits = x->trailing_bits | y->trailing_bits;
    return ret;
}

IntBitSet *intBitSetXor(IntBitSet *const x, IntBitSet *const y) {
    register word_t *xbase;
    register word_t *xend;
    register word_t *ybase;
    register word_t *retbase;
    register IntBitSet * ret = malloc(sizeof (IntBitSet));
    ret->allocated = intBitSetAdaptMax(x, y);
    xbase = x->bitset;
    xend = x->bitset+ret->allocated;
    ybase = y->bitset;
    retbase = ret->bitset = malloc(wordbytesize * ret->allocated);
    ret->size = -1;
    ret->tot = -1;
    for (; xbase < xend; ++xbase, ++ybase, ++retbase)
        *(retbase) = *(xbase) ^ *(ybase);
    ret->trailing_bits = x->trailing_bits ^ y->trailing_bits;
    return ret;
}

IntBitSet *intBitSetIntersection(IntBitSet *const x, IntBitSet *const y) {
    register word_t *xbase;
    register word_t *xend;
    register word_t *ybase;
    register word_t *retbase;
    register IntBitSet * ret = malloc(sizeof (IntBitSet));
    ret->allocated = intBitSetAdaptMin(x, y);
    xbase = x->bitset;
    xend = x->bitset+ret->allocated;
    ybase = y->bitset;
    retbase = ret->bitset = malloc(wordbytesize * ret->allocated);
    ret->size = -1;
    ret->tot = -1;
    for (; xbase < xend; ++xbase, ++ybase, ++retbase)
        *(retbase) = *(xbase) & *(ybase);
    ret->trailing_bits = x->trailing_bits & y->trailing_bits;
    return ret;
}

IntBitSet *intBitSetSub(IntBitSet *const x, IntBitSet *const y) {
    register word_t *xbase;
    register word_t *ybase;
    register word_t *retbase;
    register word_t *retend;
    register IntBitSet * ret = malloc(sizeof (IntBitSet));
    register int tmpsize = intBitSetAdaptMin(x, y);
    ret->allocated = x->allocated > tmpsize ? x->allocated : tmpsize;
    xbase = x->bitset;
    ybase = y->bitset;
    retbase = ret->bitset = malloc(wordbytesize * ret->allocated);
    retend = ret->bitset+tmpsize;
    ret->size = -1;
    ret->tot = -1;
    for (; retbase < retend; ++xbase, ++ybase, ++retbase)
        *(retbase) = *(xbase) & ~*(ybase);
    retend = ret->bitset+ret->allocated;
    for (; retbase < retend; ++xbase, ++retbase)
        *retbase = *xbase & ~y->trailing_bits;
    ret->trailing_bits = x->trailing_bits & ~y->trailing_bits;
    return ret;
}

IntBitSet *intBitSetIUnion(IntBitSet *const dst, IntBitSet *const src) {
    register word_t *dstbase;
    register word_t *srcbase;
    register word_t *srcend;
    register int allocated = intBitSetAdaptMax(dst, src);
    dstbase = dst->bitset;
    srcbase = src->bitset;
    srcend = src->bitset + allocated;
    for (; srcbase < srcend; ++dstbase, ++srcbase)
        *dstbase |= *srcbase;
    dst->size = -1;
    dst->tot = -1;
    dst->trailing_bits |= src->trailing_bits;
    return dst;
}

IntBitSet *intBitSetIXor(IntBitSet *const dst, IntBitSet *const src) {
    register word_t *dstbase;
    register word_t *srcbase;
    register word_t *srcend;
    register int allocated = intBitSetAdaptMax(dst, src);
    dstbase = dst->bitset;
    srcbase = src->bitset;
    srcend = src->bitset + allocated;
    for (; srcbase < srcend; ++dstbase, ++srcbase)
        *dstbase ^= *srcbase;
    dst->size = -1;
    dst->tot = -1;
    dst->trailing_bits ^= src->trailing_bits;
    return dst;
}

IntBitSet *intBitSetIIntersection(IntBitSet *const dst, IntBitSet *const src) {
    register word_t *dstbase;
    register word_t *srcbase;
    register word_t *dstend;
    dst->allocated = intBitSetAdaptMin(dst, src);
    dstbase = dst->bitset;
    srcbase = src->bitset;
    dstend = dst->bitset + dst->allocated;
    for (; dstbase < dstend; ++dstbase, ++srcbase)
        *dstbase &= *srcbase;
    dst->size = -1;
    dst->tot = -1;
    dst->trailing_bits &= src->trailing_bits;
    return dst;
}

IntBitSet *intBitSetISub(IntBitSet *const dst, IntBitSet *const src) {
    register word_t *dstbase;
    register word_t *srcbase;
    register word_t *dstend;
    register int allocated = intBitSetAdaptMin(dst, src);
    dstbase = dst->bitset;
    srcbase = src->bitset;
    dstend = dst->bitset + allocated;
    for (; dstbase < dstend; ++dstbase, ++srcbase)
        *dstbase &= ~*srcbase;
    dstend = dst->bitset + dst->allocated;
    for (; dstbase < dstend; ++dstbase)
        *dstbase &= ~src->trailing_bits;
    dst->size = -1;
    dst->tot = -1;
    dst->trailing_bits &= ~src->trailing_bits;
    return dst;
}

int intBitSetGetNext(const IntBitSet *const x, register int last) {
    register word_t* base = x->bitset + (++last / wordbitsize);
    register int i = last % wordbitsize;
    register word_t *end = x->bitset + x->allocated;
    while(base < end) {
        if (*base)
            for (; i<wordbitsize; ++i)
                if ((*base & ((word_t) 1 << (word_t) i)))
                    return (int) i + (int) (base - x->bitset) * wordbitsize;
        i = 0;
        ++base;
    }
    return x->trailing_bits ? last : -2;
}

unsigned char intBitSetCmp(IntBitSet *const x, IntBitSet *const y) {
    register word_t *xbase;
    register word_t *xend;
    register word_t *ybase;
    register unsigned char ret = 0;
    register int allocated = intBitSetAdaptMax(x, y);
    xbase = x->bitset;
    xend = x->bitset+allocated;
    ybase = y->bitset;
    for (; ret != 3 && xbase<xend; ++xbase, ++ybase)
        ret |= (*ybase != (*xbase | *ybase)) * 2 + (*xbase != (*xbase | *ybase));
    ret |= (y->trailing_bits != (x->trailing_bits | y->trailing_bits)) * 2 + (x->trailing_bits != (x->trailing_bits | y->trailing_bits));
    return ret;
}
