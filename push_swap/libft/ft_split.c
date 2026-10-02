/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wgulinsk <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/07 17:12:56 by wgulinsk          #+#    #+#             */
/*   Updated: 2025/10/07 17:13:00 by wgulinsk         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
#include <stdlib.h>

static size_t	ft_count(char const *s, char c)
{
	size_t	i;
	size_t	count;

	i = 0;
	count = 0;
	while (s[i] != '\0')
	{
		while (s[i] == c)
			i++;
		if (s[i] != '\0')
		{
			count++;
			while (s[i] != '\0' && s[i] != c)
				i++;
		}
	}
	return (count);
}

static int	ft_free(char **res, size_t ind)
{
	while (ind--)
		free(res[ind]);
	free(res);
	return (0);
}

static int	ft_helper(char **res, char const *s, char c)
{
	size_t	i;
	size_t	ind;
	size_t	pom;

	i = 0;
	ind = 0;
	while (s[i] != '\0')
	{
		if (s[i] != c)
		{
			pom = i;
			while (s[i] != c && s[i] != '\0')
				i++;
			res[ind] = ft_substr(s, pom, i - pom);
			if (!res[ind++])
				return (ft_free(res, ind - 1));
		}
		else
			i++;
	}
	res[ind] = NULL;
	return (1);
}

char	**ft_split(char const *s, char c)
{
	char	**res;

	if (s == NULL)
		return (NULL);
	res = (char **)malloc((ft_count(s, c) + 1) * sizeof (char *));
	if (res == NULL)
		return (NULL);
	if (ft_helper(res, s, c) != 1)
		return (NULL);
	return (res);
}
