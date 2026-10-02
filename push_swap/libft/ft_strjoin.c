/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strjoin.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wgulinsk <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/01 14:46:25 by wgulinsk          #+#    #+#             */
/*   Updated: 2025/10/01 14:46:28 by wgulinsk         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
#include <stdlib.h>

char	*ft_strjoin(char const *s1, char const *s2)
{
	size_t	i;
	char	*pom;
	size_t	len_s1;
	size_t	len_s2;

	i = 0;
	len_s1 = ft_strlen(s1);
	len_s2 = ft_strlen(s2);
	pom = malloc(ft_strlen(s1) + ft_strlen(s2) + 1);
	if (pom == NULL || (s1 == NULL && s2 == NULL))
		return (NULL);
	while (i < len_s1)
	{
		pom[i] = s1[i];
		i++;
	}
	i = 0;
	while (i < len_s2)
	{
		pom[i + len_s1] = s2[i];
		i++;
	}
	pom[len_s1 + len_s2] = '\0';
	return (pom);
}
