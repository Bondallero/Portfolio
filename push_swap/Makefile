NAME = push_swap

CC = cc
CFLAGS = -Wall -Wextra -Werror
RE = rm -f

SRC = main.c big_sort.c build_stack.c indexation.c push.c rotate.c swap.c rrotate.c small_sort.c sort_utils.c valid_utils.c free.c
LIBFT_DIR = ./libft
LIBFT = $(LIBFT_DIR)/libft.a

OBJ = $(SRC:.c=.o)

all: $(NAME)

$(LIBFT):
	make -C $(LIBFT_DIR)

$(NAME): $(OBJ) $(LIBFT)
	$(CC) $(CFLAGS) $(OBJ) $(LIBFT) -o $(NAME)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	$(RE) $(OBJ)
	make -C $(LIBFT_DIR) clean

fclean: clean
	$(RE) $(NAME)
	make -C $(LIBFT_DIR) fclean

re: fclean all

.PHONY: all clean fclean re
