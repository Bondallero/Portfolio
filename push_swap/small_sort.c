/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   small_sort.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wgulinsk <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/03 19:19:09 by wgulinsk          #+#    #+#             */
/*   Updated: 2026/07/03 19:19:12 by wgulinsk         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	sort_2_elements(t_stack **a)
{
	if ((*a)->value >= (*a)->next->value)
		sa(a);
}

void	sort_3_elements(t_stack **a)
{
	int	val_1;
	int	val_2;
	int	val_3;

	val_1 = (*a)->value;
	val_2 = (*a)->next->value;
	val_3 = (*a)->next->next->value;
	if (val_1 > val_2 && val_2 < val_3 && val_1 < val_3)
		sa(a);
	else if (val_1 > val_2 && val_2 > val_3)
	{
		sa(a);
		rra(a);
	}
	else if (val_1 > val_2 && val_2 < val_3 && val_1 > val_3)
		ra(a);
	else if (val_1 < val_2 && val_2 > val_3 && val_1 < val_3)
	{
		sa(a);
		ra(a);
	}
	else if (val_1 < val_2 && val_2 > val_3 && val_1 > val_3)
		rra(a);
}

void	sort_5_elements(t_stack **a, t_stack **b)
{
	while (find_size(*a) > 3 && find_size(*a) < 6)
	{
		move_max(a);
		pb(a, b);
	}
	sort_3_elements(a);
	if (find_size(*b) == 1)
	{
		pa(a, b);
		ra(a);
	}
	if (find_size(*b) == 2)
	{
		if ((*b)->value < (*b)->next->value)
			sb(b);
		while (*b)
			pa(a, b);
		ra(a);
		ra(a);
	}
}
