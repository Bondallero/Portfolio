/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   big_sort.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wgulinsk <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/03 19:17:39 by wgulinsk          #+#    #+#             */
/*   Updated: 2026/07/03 19:17:42 by wgulinsk         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	big_sort(t_stack **a, t_stack **b)
{
	int	size;
	int	max_bits;
	int	i;
	int	j;

	size = find_size(*a);
	max_bits = count_max_bits(*a);
	i = 0;
	while (i < max_bits)
	{
		j = 0;
		while (j < size)
		{
			if ((((*a)->index >> i) & 1) == 1)
				ra(a);
			else
				pb(a, b);
			j++;
		}
		while (*b)
			pa(a, b);
		i++;
	}
}

void	sort_main(t_stack **a, t_stack **b)
{
	int	size;

	size = find_size(*a);
	if (size == 2)
		sort_2_elements(a);
	else if (size == 3)
		sort_3_elements(a);
	else if (size <= 5)
		sort_5_elements(a, b);
	else
		big_sort(a, b);
}
