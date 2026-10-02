/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   valid_utils.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wgulinsk <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/03 19:19:42 by wgulinsk          #+#    #+#             */
/*   Updated: 2026/07/03 19:19:44 by wgulinsk         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	count_words(int argc, char **argv)
{
	int		i;
	int		count;
	char	**tmp;
	int		j;

	i = 1;
	count = 0;
	while (i < argc)
	{
		tmp = ft_split(argv[i], ' ');
		if (!tmp)
			return (0);
		j = 0;
		while (tmp[j])
		{
			count++;
			j++;
		}
		free_arr(tmp);
		i++;
	}
	return (count);
}

char	**fill_args(int argc, char **argv, char **res)
{
	int		i;
	int		j;
	int		k;
	char	**tmp;

	i = 1;
	k = 0;
	while (i < argc)
	{
		tmp = ft_split(argv[i], ' ');
		if (!tmp)
		{
			res[k] = NULL;
			free_arr(res);
			return (NULL);
		}
		j = 0;
		while (tmp[j])
			res[k++] = tmp[j++];
		free(tmp);
		i++;
	}
	res[k] = NULL;
	return (res);
}

char	**split_args(int argc, char **argv)
{
	char	**res;
	int		size;

	size = count_words(argc, argv);
	if (size == 0)
		return (NULL);
	res = malloc(sizeof(char *) * (size + 1));
	if (!res)
		return (NULL);
	if (!fill_args(argc, argv, res))
		return (NULL);
	return (res);
}

static int	ft_atoi_helper(char *s, int i, int sign, int *error)
{
	long long	n;

	n = 0;
	while (s[i])
	{
		if (s[i] < '0' || s[i] > '9')
			return (*error = 1, 0);
		n = n * 10 + (s[i] - '0');
		if ((n * sign) > 2147483647 || (n * sign) < -2147483648)
			return (*error = 1, 0);
		i++;
	}
	return ((int)(n * sign));
}

int	ft_ult_atoi(char *s, int *error)
{
	int		sign;
	int		i;

	*error = 0;
	sign = 1;
	i = 0;
	if (s[i] == '-' || s[i] == '+')
	{
		if (s[i] == '-')
			sign = -1;
		i++;
	}
	if (!s[i])
		return (*error = 1, 0);
	return (ft_atoi_helper(s, i, sign, error));
}
