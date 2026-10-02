/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wgulinsk <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/03 19:15:17 by wgulinsk          #+#    #+#             */
/*   Updated: 2026/07/03 19:16:57 by wgulinsk         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include <stdlib.h>
# include <unistd.h>
# include "libft/libft.h"

typedef struct s_stack
{
	int				value;
	int				index;
	struct s_stack	*next;
}	t_stack;

//stack assemble
t_stack	*ft_add_node(int value);
void	ft_add_back(t_stack **stack, t_stack *new);
void	ft_free_stack(t_stack **stack);
int		ft_dup_check(t_stack *stack, int value);
t_stack	*build_stack(char **args);

//input checking and stuff
void	free_arr(char **arr);
int		count_words(int argc, char **argv);
char	**fill_args(int argc, char **argv, char **res);
char	**split_args(int argc, char **argv);
int		ft_ult_atoi(char *s, int *error);
int		ft_error(void);

//sorting
void	sort_2_elements(t_stack **a);
void	sort_3_elements(t_stack **a);
void	sort_5_elements(t_stack **a, t_stack **b);
void	big_sort(t_stack **a, t_stack **b);
void	sort_main(t_stack **a, t_stack **b);

//indexation
int		count_max_bits(t_stack *a);
void	stack_indexation(t_stack *a);
void	arr_indexation(t_stack *a, int *ind, int size);
void	sort_array(int *arr, int size);
int		*copy_to_arr(t_stack *a);

//helpers
void	free_stack(t_stack **stack);
int		find_max(t_stack *stack);
int		find_max_pos(t_stack *stack);
int		find_size(t_stack *stack);
int		is_sorted(t_stack *stack);
void	move_max(t_stack **stack);

//operations
void	pa(t_stack **stack_a, t_stack **stack_b);
void	pb(t_stack **stack_a, t_stack **stack_b);
void	sa(t_stack **stack_a);
void	sb(t_stack **stack_a);
void	ss(t_stack **stack_a, t_stack **stack_b);
void	ra(t_stack **stack_a);
void	rb(t_stack **stack_a);
void	rr(t_stack **stack_a, t_stack **stack_b);
void	rra(t_stack **stack_a);
void	rrb(t_stack **stack_a);
void	rrr(t_stack **stack_a, t_stack **stack_b);

#endif
