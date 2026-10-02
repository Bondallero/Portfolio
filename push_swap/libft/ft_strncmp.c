/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   strncmp.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: wgulinsk <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/07/07 15:10:01 by wgulinsk          #+#    #+#             */
/*   Updated: 2025/07/07 15:10:04 by wgulinsk         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
#include <unistd.h>

int	ft_strncmp(char *s1, char *s2, unsigned int n)
{
	unsigned int	i;

	i = 0;
	while (i < n && (s1[i] != '\0' || s2[i] != '\0'))
	{
		if ((char)s1[i] != (char)s2[i])
		{
			if (!ft_isascii(s1[i]))
				return ((char)s2[i] - (char)s1[i]);
			else
				return ((char)s1[i] - (char)s2[i]);
		}
		i++;
	}
	return (0);
}
