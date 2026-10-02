/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wgulinsk <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/03 19:18:28 by wgulinsk          #+#    #+#             */
/*   Updated: 2026/07/03 19:18:30 by wgulinsk         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	ft_error(void)
{
	ft_putstr_fd("Error\n", 2);
	return (1);
}

void	free_stack(t_stack **stack)
{
	t_stack	*help;

	while (*stack)
	{
		help = (*stack)->next;
		free(*stack);
		*stack = help;
	}
}

int	main(int argc, char **argv)
{
	char	**args;
	t_stack	*a;
	t_stack	*b;

	b = NULL;
	if (argc < 2)
		return (0);
	args = split_args(argc, argv);
	if (!args)
		return (ft_error());
	a = build_stack(args);
	free_arr(args);
	if (!a)
		return (ft_error());
	if (!is_sorted(a))
	{
		stack_indexation(a);
		sort_main(&a, &b);
	}
	free_stack(&a);
	free_stack(&b);
	return (0);
}
