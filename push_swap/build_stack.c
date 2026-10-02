/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   build_stack.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wgulinsk <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/03 19:18:07 by wgulinsk          #+#    #+#             */
/*   Updated: 2026/07/03 19:18:09 by wgulinsk         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_stack	*ft_add_node(int value)
{
	t_stack	*node;

	node = malloc(sizeof(t_stack));
	if (!node)
		return (NULL);
	node->value = value;
	node->next = NULL;
	return (node);
}

void	ft_add_back(t_stack **stack, t_stack *new)
{
	t_stack	*current;

	if (!*stack)
	{
		*stack = new;
		return ;
	}
	current = *stack;
	while (current->next)
		current = current->next;
	current->next = new;
}

int	ft_dup_check(t_stack *stack, int value)
{
	while (stack)
	{
		if (stack->value == value)
			return (1);
		stack = stack->next;
	}
	return (0);
}

t_stack	*build_stack(char **args)
{
	t_stack	*stack;
	int		i;
	int		error;
	int		value;

	stack = NULL;
	i = 0;
	while (args[i])
	{
		value = ft_ult_atoi(args[i], &error);
		if (error == 1 || ft_dup_check(stack, value))
		{
			ft_free_stack(&stack);
			return (NULL);
		}
		ft_add_back(&stack, ft_add_node(value));
		if (!stack)
			return (NULL);
		i++;
	}
	return (stack);
}
