/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wgulinsk <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/07 17:43:50 by wgulinsk          #+#    #+#             */
/*   Updated: 2025/10/07 17:43:52 by wgulinsk         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
#include <unistd.h>

static void	ft_reverse(char *str, int len)
{
	int		i;
	char	pom;
	int		j;

	i = 0;
	j = len - 1;
	while (i < j)
	{
		pom = str[i];
		str[i] = str[j];
		str[j] = pom;
		i++;
		j--;
	}
}

static int	ft_count(int n)
{
	long	pom;
	int		count;

	count = 0;
	pom = n;
	if (pom == 0)
		return (1);
	if (pom < 0)
	{
		pom = -pom;
		count++;
	}
	while (pom > 0)
	{
		pom = pom / 10;
		count++;
	}
	return (count);
}

static int	ft_helper(char *res, size_t n)
{
	size_t	i;

	i = 0;
	if (n == 0)
		res[i++] = '0';
	while (n > 0)
	{
		res[i++] = (n % 10) + '0';
		n = n / 10;
	}
	return (i);
}

char	*ft_itoa(int n)
{
	int		i;
	char	*res;
	int		sign;
	long	pom;

	pom = n;
	sign = 1;
	res = (char *)malloc(ft_count(n) + 1);
	if (res == NULL)
		return (NULL);
	if (pom < 0)
	{
		pom = -pom;
		sign = -1;
	}
	i = ft_helper(res, pom);
	if (sign == -1)
		res[i++] = '-';
	ft_reverse(res, i);
	res[i] = '\0';
	return (res);
}
