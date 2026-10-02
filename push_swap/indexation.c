/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   indexation.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wgulinsk <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/03 19:18:17 by wgulinsk          #+#    #+#             */
/*   Updated: 2026/07/03 19:18:19 by wgulinsk         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	*copy_to_arr(t_stack *a)
{
	int	*arr;
	int	i;
	int	size;

	i = 0;
	size = find_size(a);
	arr = malloc(sizeof(int) * size);
	if (!arr)
		return (NULL);
	while (a)
	{
		arr[i++] = a->value;
		a = a->next;
	}
	return (arr);
}

void	sort_array(int *arr, int size)
{
	int	i;
	int	j;
	int	help;

	i = 0;
	while (i < size - 1)
	{
		j = 0;
		while (j < size - i - 1)
		{
			if (arr[j] > arr[j + 1])
			{
				help = arr[j];
				arr[j] = arr[j + 1];
				arr[j + 1] = help;
			}
			j++;
		}
		i++;
	}
}

void	arr_indexation(t_stack *a, int *ind, int size)
{
	int	i;

	while (a)
	{
		i = 0;
		while (i < size)
		{
			if (a->value == ind[i])
			{
				a->index = i;
				break ;
			}
			i++;
		}
		a = a->next;
	}
}

void	stack_indexation(t_stack *a)
{
	int	*arr;
	int	size;

	size = find_size(a);
	arr = copy_to_arr(a);
	if (!arr)
		return ;
	sort_array(arr, size);
	arr_indexation(a, arr, size);
	free(arr);
}

int	count_max_bits(t_stack *a)
{
	int	max_index;
	int	count;

	max_index = find_size(a) - 1;
	count = 0;
	while ((max_index >> count) != 0)
		count++;
	return (count);
}
