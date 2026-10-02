/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strnstr.c                                        :+:      :+:    :+:  */
/*                                                    +:+ +:+         +:+     */
/*   By: wgulinsk <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/09/25 15:24:12 by wgulinsk          #+#    #+#             */
/*   Updated: 2025/09/25 15:24:14 by wgulinsk         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
#include <unistd.h>

char	*ft_strnstr(const char *s, const char *c, size_t n)
{
	size_t	i;
	size_t	j;

	i = 0;
	if (c[i] == '\0')
	{
		return ((char *)s);
	}
	while (i < n && s[i])
	{
		j = 0;
		while (s[i + j] == c[j] && (i + j) < n && c[j] != '\0')
		{
			j++;
		}
		if (c[j] == '\0')
		{
			return ((char *)&s[i]);
		}
		i++;
	}
	return (NULL);
}
