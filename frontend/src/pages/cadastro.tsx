import { useState, FormEvent } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

import { AuthLayout } from '@/components/AuthLayout';
import { Input } from '@/components/Input';
import { Label } from '@/components/Label';
import { Field } from '@/components/Field';
import { Button } from '@/components/Button';
import { Logo } from '@/components/Logo';
import { Heading } from '@/components/Heading';
import { Text, TextLink } from '@/components/Text';

const Cadastro = () => {
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [mensagem, setMensagem] = useState('');
  const [erro, setErro] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setErro('');
    setMensagem('');

    try {
      const response = await axios.post('http://localhost:8000/usuarios/', {
        nome,
        email,
      });

      const senha = response.data?.senha_gerada;
      setMensagem(`Usuário cadastrado com sucesso! Senha gerada: ${senha}`);

      setTimeout(() => {
        navigate('/login');
      }, 4000);
    } catch (err: any) {
      if (axios.isAxiosError(err)) {
        setErro(err.response?.data?.detail || 'Erro ao cadastrar.');
      } else {
        setErro('Erro inesperado.');
      }
    }
  };

  return (
    <AuthLayout>
      <form onSubmit={handleSubmit} className="grid w-full max-w-sm grid-cols-1 gap-6">
        <Logo className="mx-auto" />
        <Heading className="text-center">Cadastro de Usuário</Heading>

        <Field>
          <Label htmlFor="nome">Nome completo</Label>
          <Input
            id="nome"
            name="nome"
            type="text"
            value={nome}
            onChange={(e) => setNome(e.target.value)}
            required
          />
        </Field>

        <Field>
          <Label htmlFor="email">E-mail</Label>
          <Input
            id="email"
            name="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </Field>

        <Button type="submit">Cadastrar</Button>

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
          Já tem conta? <TextLink href="/login">Voltar para o login</TextLink>
        </Text>
      </form>
    </AuthLayout>
  );
};

export default Cadastro;
