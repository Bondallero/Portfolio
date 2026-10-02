/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memmove.c                                        :+:      :+:    :+:  */
/*                                                    +:+ +:+         +:+     */
/*   By: wgulinsk <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/09/25 15:24:12 by wgulinsk          #+#    #+#             */
/*   Updated: 2025/09/25 15:24:14 by wgulinsk         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
#include <unistd.h>

void	*ft_memmove(void *dest, const void *src, size_t n)
{
	const unsigned char	*p2;
	unsigned char		*p1;

	p1 = (unsigned char *)dest;
	p2 = (const unsigned char *)src;
	if (p1 == p2 || n == 0)
	{
		return (dest);
	}
	if (p1 < p2)
	{
		while (n--)
			*p1++ = *p2++;
	}
	else
	{
		p1 += n;
		p2 += n;
		while (n--)
			*--p1 = *--p2;
	}
	return (dest);
}
