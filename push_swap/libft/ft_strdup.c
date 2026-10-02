/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wgulinsk <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/07/17 12:51:48 by wgulinsk          #+#    #+#             */
/*   Updated: 2025/07/17 12:51:50 by wgulinsk         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
#include <stdlib.h>

char	*ft_strdup(char *src)
{
	int		l;
	int		i;
	char	*dest;

	l = 0;
	i = 0;
	while (src[l] != '\0')
	{
		l++;
	}
	dest = (char *)malloc(sizeof(char ) * (l + 1));
	if (!dest)
	{
		return (NULL);
	}
	while (i < l)
	{
		dest[i] = src[i];
		i++;
	}
	dest[i] = '\0';
	return (dest);
}
