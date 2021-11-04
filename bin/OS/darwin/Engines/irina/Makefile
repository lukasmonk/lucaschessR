LINK_TARGET = Irina-0.14

OBJS = main.o loop.o board.o data.o util.o movegen.o makemove.o perft.o eval.o evalst.o search.o person.o hash.o book.o

REBUILDABLES = $(OBJS) $(LINK_TARGET)

clean :
	rm -f $(REBUILDABLES)
	echo Clean done

all : $(LINK_TARGET)
	echo All done

$(LINK_TARGET) : $(OBJS)
	gcc -O3 -arch arm64 -arch x86_64 -o $@ $^  -DNDEBUG
	strip $(LINK_TARGET)

%.o : %.c
	gcc -Wall -O3 -arch arm64 -arch x86_64 -o $@ -c $< -DNDEBUG
