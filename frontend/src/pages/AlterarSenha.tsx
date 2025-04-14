import { useState, FormEvent } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

import { AuthLayout } from '@/components/AuthLayout';
import { Input } from '@/components/Input';
import { Label } from '@/components/Label';
import { Field } from '@/components/Field';
import { Button } from '@/components/Button';
import { Heading } from '@/components/Heading';
import { Text, TextLink } from '@/components/Text';
import { Logo } from '@/components/Logo';

const AlterarSenha = () => {
  const [novaSenha, setNovaSenha] = useState('');
  const [mensagem, setMensagem] = useState('');
  const [erro, setErro] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setMensagem('');
    setErro('');

    const token = localStorage.getItem('token');

    try {
      await axios.post(
        'http://localhost:8000/usuarios/alterar-senha',
        { nova_senha: novaSenha },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      // ✅ Define flag para não mostrar o pop-up de novo
      localStorage.setItem('senha_alterada', 'true');

      setMensagem('Senha alterada com sucesso!');
      setTimeout(() => {
        navigate('/dashboard');
      }, 3000);
    } catch (err: any) {
      if (axios.isAxiosError(err)) {
        setErro(err.response?.data?.detail || 'Erro ao alterar a senha.');
      } else {
        setErro('Erro inesperado. Tente novamente.');
      }
    }
  };

  return (
    <AuthLayout>
      <form
        onSubmit={handleSubmit}
        className="grid w-full max-w-sm grid-cols-1 gap-6"
      >
        <Logo className="mx-auto" />
        <Heading className="text-center">Alterar Senha</Heading>

        <Field>
          <Label htmlFor="novaSenha">Nova Senha</Label>
          <Input
            id="novaSenha"
            type="password"
            value={novaSenha}
            onChange={(e) => setNovaSenha(e.target.value)}
            required
          />
        </Field>

        <Button type="submit">Alterar Senha</Button>

        {mensagem && (
          <p className="text-sm text-green-700 text-center bg-green-100 p-2 rounded">
            {mensagem}
          </p>
        )}
        {erro && (
          <p className="text-sm text-red-700 text-center bg-red-100 p-2 rounded">
            {erro}
          </p>
        )}

        <Text className="text-center">
          <TextLink href="/dashboard">Voltar para o dashboard</TextLink>
        </Text>
      </form>
    </AuthLayout>
  );
};

export default AlterarSenha;
