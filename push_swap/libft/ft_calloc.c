/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_calloc.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wgulinsk <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/07/17 12:51:48 by wgulinsk          #+#    #+#             */
/*   Updated: 2025/07/17 12:51:50 by wgulinsk         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
#include <stdlib.h>

void	*ft_calloc(size_t nmemb, size_t size)
{
	unsigned char	*pom;
	size_t			i;

	i = 0;
	if (size != 0 && nmemb > (size_t)-1 / size)
		return (NULL);
	if (nmemb * size == 0)
		pom = (unsigned char *)malloc(1);
	else
		pom = (unsigned char *)malloc(nmemb * size);
	if (pom == NULL)
	{
		return (NULL);
	}
	else
	{
		while (i < nmemb * size)
			pom[i++] = 0;
	}
	return (pom);
}
