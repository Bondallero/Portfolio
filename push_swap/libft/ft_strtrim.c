/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strtrim.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wgulinsk <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/07 17:03:45 by wgulinsk          #+#    #+#             */
/*   Updated: 2025/10/07 17:03:50 by wgulinsk         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
#include <stdlib.h>

static char	*ft_strncpy(char *dest, const char *src, size_t n)
{
	size_t	i;

	i = 0;
	while (i < n)
	{
		dest[i] = src[i];
		i++;
	}
	dest[i] = '\0';
	return (dest);
}

char	*ft_strtrim(char const *s1, char const *set)
{
	char	*res;
	size_t	p1;
	size_t	p2;

	p1 = 0;
	p2 = ft_strlen(s1);
	if (s1 == NULL)
		return (NULL);
	else if (set == NULL)
	{
		res = (char *)malloc(p2 + 1);
		ft_strncpy(res, s1 + p1, p2);
	}
	else
	{
		while (s1[p1] && ft_strchr(set, s1[p1]))
			p1++;
		while (p2 > p1 && ft_strchr(set, s1[p2 - 1]))
			p2--;
		res = (char *)malloc(p2 - p1 + 1);
		if (res == NULL)
			return (NULL);
		ft_strncpy(res, s1 + p1, p2 - p1);
	}
	return (res);
}
